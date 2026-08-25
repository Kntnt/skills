# model-selector capture

## NAME

model-selector capture - opt in to automatic local run-evidence capture

## SYNOPSIS

**/model-selector** **capture** **--on** [**--harness=**_NAME_] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--off** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--review=**_IDENTITY_ **--action=save**|**--action=failed**|**--action=ignore** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Turn ordinary work in a supported Harness into local evidence without anyone remembering to collect it. `record` imports a prepared observation and `observe` prepares one for deliberately routed work; neither covers the ordinary case, where the measurements that should eventually replace public benchmark priors are simply never written down.

Capture is an explicit opt-in of an Enabled Skill rather than a consequence of enabling one, because it installs persistent local lifecycle integration and handles local metadata. **--on** states what it installs, what categories of metadata it retains, how that data is cleaned up, and how to turn it off, then installs one owned integration per named Harness and verifies the result from disk. Nothing is captured before that consent, and nothing that was already accepted is lost after it is withdrawn.

While capture is on, a small draft is created when substantive work begins in a session and updated only from lifecycle, usage, checker, quota, and latency signals. At an eligible completion boundary the draft becomes exactly one normalized observation and is imported into the existing evidence ledger, rebuilding only the derived frontiers whose eligible run set actually changed; the draft is then deleted. Ordinary work is not routed, so its observation records the exact main seat it inherited rather than a point somebody chose.

An outcome is established from outside the work or not at all. An objective checker, a frozen rubric, a declared failure signal, or the user's own confirmation may establish one; model self-confidence never does. Work that offers none waits in a bounded pending-review store until **--review** answers it or retention removes it, and an infrastructure error keeps its own outcome so that a broken environment can never lower a configuration's measured quality.

The synchronous hook path does bounded local metadata I/O and nothing else: no network request, no model call, no test run, no repository-wide hashing, no transcript scan, and no long-lived background work. It is fail-open, so a capture that cannot run costs the session nothing. Notifications are user-facing and debounced, and are never injected into the context of the model being measured.

## OPTIONS

**--on**

Consent to automatic capture and install the owned integration into each Harness named by **--harness**, defaulting to every supported Harness detected. Repeating it repairs and converges rather than installing twice. A Harness whose supported lifecycle cannot carry the contract reports an Unsatisfied integration capability and is never reported healthy.

**--off**

Stop capture and remove every hook and adapter this feature owns, verifying the result from disk per Harness. Accepted evidence is preserved: turning a measurement off is not a reason to forget what it measured. Making the Skill Disabled does the same thing, so there is no second shutdown step to remember; an explicit purge of captured data, if ever wanted, remains a separate act.

**--status**

Report whether capture is enabled, adapter health per Harness, the pending-review count, the oldest pending age, storage in use, and the retention bounds. It reconciles abandoned drafts as it passes and performs no network access or evaluation.

**--review=**_IDENTITY_

Settle one pending capture named by the opaque identity `--status` lists. Requires **--action**.

**--action=save**, **--action=failed**, **--action=ignore**

Answer a deferred review: record the work as a success, record it as a failure, or discard the capture without recording anything. A saved or failed outcome carries explicit user confirmation as its authority, which is what makes it evidence at all.

**--harness=**_NAME_

Name a Harness to install into, repeatable. Supported values are `claude-code`, `codex`, and `opencode`. Without it, every supported Harness is installed into. The installed hook carries the Harness it was written for, so nothing later has to guess which one ran it.

**--data=**_PATH_

Use *PATH* as the data directory instead of `~/.model-selector/`. The capture store, the evidence ledger, and the derived frontiers all live under the selected directory.

## RETAINED DATA

Only what an observation is built from: opaque session and task identity, timestamps and Harness identity, the exact resolved model, deliberation control, serving mode and access channel, tool and policy fingerprints, checker identity and result, available token categories, tool counts, retries, fallbacks, provider bill, quota deltas, wall and first-useful-output latency, provenance, and sanitized artifact hashes.

Never full prompts, responses, reasoning, source files, diffs, terminal output, secrets, credentials, or complete Harness transcripts, and never an absolute path where an opaque identity is sufficient. Fields are copied onto an allow-list rather than stripped afterwards, so nothing forbidden enters by sitting beside something wanted.

## RETENTION

An imported capture is deleted immediately, and an empty or irrelevant draft is discarded. Pending and failed captures are kept at most 30 days, 100 drafts, and 1 MiB in total; whichever bound is exceeded, the oldest go first. Cleanup is deterministic and runs at a session start or a status pass rather than from a daemon. Accepted evidence is never subject to these bounds.

## OUTPUT

One JSON object. **--on** names the consent it obtained and each Harness's installation result; **--off** names each Harness's removal result; **--status** answers the five questions above; **--review** names what was imported or discarded.

## DIAGNOSTICS

An unsupported Harness is reported as an Unsatisfied integration capability rather than silently skipped. An installation or removal that only partly applied is reported per Harness and never as a complete one. A failure inside the hook path is swallowed by design and never reaches the session it was called from.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the shipped offline capture module. The owned lifecycle integration requires Claude Code, Codex, or OpenCode; any other Harness reports the capability Unsatisfied.

## SEE ALSO

**/model-selector record --help**, **/model-selector observe --help**, **/model-selector status --help**
