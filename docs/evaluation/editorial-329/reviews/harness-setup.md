# Native GPT harness preparation for #338

Verified on 2026-09-19. This preparation ran one access/isolation probe, no
editorial fixture. It makes no claim that the evaluation matrix has passed.

## Observed identity and access

The parent session's native rollout
`rollout-2026-09-19T19-59-11-01a0bad2-7a37-7d53-80a8-0c909db58d6c.jsonl`
exposes `model: gpt-6-astra`, `effort: high` in `turn_context`. The preparation
subagent and isolated access probe expose the same values. These are observed
identifiers, not a translation of “Astra Hi”.

`/opt/homebrew/bin/codex` is a symlink to the native executable
`/opt/homebrew/Caskroom/codex/0.155.1/bin/codex`; its version is
`codex-cli 0.155.1`. No Codex shim was encountered on the effective PATH.
`features list` reports `multi_agent` stable/true. The probe completed with
`ACCESS_OK` and reported the fresh `collaboration.spawn_agent` capability. It
was instructed not to spawn and did not spawn.

The private config retains the observed model and effort and the user's
observed service tier (`default`). Authentication was copied privately into
the temporary Codex home. Credentials are never repository deliverables.
No user plugins, MCP configuration, memory or rules were copied.

Evidence is in [the exact command and environment](../harness/probe-command.json),
[native context](../harness/probe-native-context.json),
[event trace](../harness/probe-trace.jsonl),
[final response](../harness/probe-response.txt) and
[stderr](../harness/probe-stderr.txt).

## Isolation and dispatch

The probe used a private home, Codex home, Git repository, temporary directory,
UV cache and XDG data/cache areas. It started a new `codex exec`, without resume,
fork or inherited conversation. `CODEX_SESSION_ID` and `CODEX_THREAD_ID` were
removed from the child environment.

Only Write, Redline, Proofread and Manager were copied into the project's
`.agents/skills/`. The actual injected catalogue contains the local Write and
Proofread and five CLI system skills under the private Codex home. It contains
no skill path under the user's active global installation. The CLI's system
skills are harness bootstrap files, not global editorial resources. This is
consistent with the [official discovery documentation](https://learn.chatgpt.com/docs/build-skills),
read on 2026-09-19.

Redline and Manager have `disable-model-invocation: true`, so neither appears
in the automatic skill catalogue. The runner therefore supplies the same
neutral dispatch instruction to both instruction revisions:

> For a `/write` or `/redline` invocation, read and execute the corresponding
> `.agents/skills/<name>/SKILL.md` in this project. These are the installed
> Skills for this invocation. Follow their shipped instructions.

The fixture's full formal invocation remains the user message. The dispatch
instruction supplies no editorial rule or expected result. Its exact text and
the separate scratch location are captured as harness context for each run.
Actual `SKILL.md` reads and invocation-engine calls must still be verified in
the trace. The sibling Manager is found first by `scripts/invoke.py`; the runner
clears inherited `KNTNT_*` overrides so no source path points to the live tree.

## Reusable evaluator runner

[`harness/run.py`](../harness/run.py) captures one invocation per fresh native
session. It accepts immutable instruction and corpus revisions, a complete
prompt file and a new output directory. It refuses an existing output directory
to preserve failures. For example, after the matrix is frozen:

```sh
uv run docs/evaluation/editorial-329/harness/run.py \
  --revision=8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6 \
  --corpus-revision=<frozen-corpus-commit> \
  --prompt=<evaluator-owned-prompt-file> \
  --input <source-package-or-write-artifact> \
  --input-name source.md \
  --output=<new-evaluator-output-directory>
```

The instruction installation comes from `git archive <revision>` of the four
required skill directories, including the Manager's Library. The baseline uses
`8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6`; the candidate must use the integrated
committed revision. Both use the same frozen corpus. The runner reads the model
identity from the parent's real native rollout; it accepts no model/effort
parameter. Correction subagents inherit this configuration.

Each invocation gets its own working repository, home, scratch and session
store. Model writes are confined with the native `workspace-write` sandbox to
work and scratch. The implicit system `/tmp` and `TMPDIR` allowances are disabled;
the declared scratch directory is explicitly added, and UV/XDG paths point
inside it. Network access is enabled for UV dependency provisioning. The CLI's
own session writes occur in the inventoried private home. Native stdout,
stderr and final-response captures are evaluator effects outside model-writable
areas. Exact command arguments and isolation variables are written to `run.json`.

`--input-name source.md` stages the Write source package; `--input-name input.md`
stages the Text Artifact for Redline. The runner copies the exact supplied file
into the private workspace and preserves `supplied-input.md` independently in
the evaluator output. It exposes only that input file, not its source directory.

Write and Redline are separate invocations. Supply the full Write artifact,
including metadata, to Redline, without Write's source package or delivery
commentary. Preserve the complete Write response separately. For a Redline
no-change response, the resulting artifact remains the supplied input.

The runner starts the CLI in its own process group, registers the root and PID
immediately, enforces a timeout, and preserves failure evidence. It intentionally
leaves its temporary root after capture: the evaluator removes that root with
its full literal path after inspection, as required by the session cleanup rule.
Neither active installation nor user fixture is changed.

## What every actual run must establish

Before/after inventories cover the entire private root: working copy, installed
skills, `.git`, export, home, Codex home and all scratch/cache locations. Entries
record type, mode, size, hash or symlink target. Authentication content and its
hash are withheld; a separate boolean records whether it changed. No credentials
are copied with the native session records.

Changes are enumerated, not silently excluded. Native system-skill bootstrap,
sqlite/WAL and session files are Harness effects; evaluator captures are
evaluator effects. Trace reads must distinguish them from model-created files.
A before/after inventory proves what remains, not that no transient file ever
existed: review executed commands for transient writes and cleanup too.

The runner retains stdout JSONL and **every native rollout**, including
correction-subagent sessions. Verify actual loading of common base, selected
genre, resolved language scopes, only any selected technique, and corresponding
correction-agent resources. Verify exactly one final whole-artifact Proofread
invocation and no substantive edit afterwards. A self-report is not evidence
of a file read. Record missing/ambiguous evidence rather than infer a pass.

The initial probe establishes authentication, fresh-session isolation, observed
model identity and tool availability. It did not run UV, use workspace-write,
execute the dispatch instruction or perform a correction. Those parts of the
runner must be verified in the first real run and are not yet claimed successes.

Only GPT records were consulted: `write-gpt-2026-08-26-180.md`,
`redline-gpt-2026-08-26-174.md`, and a header match in
`write-gpt-2026-08-26.md`. They document earlier CLI 0.149.1 / `gpt-5.6-sol`
methodology, not current results. No other provider's record was read and no
other provider was started. No access or authentication blocker was found.

## Probe cleanup

The registered probe root was
`/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-editorial-329-harness-nxb35u9c`.
Process-group leader `9806` had exited before cleanup. The root, including its
credential copy, was removed after capturing the declared evidence. The harness
artifacts and this report are evaluation deliverables and remain.
