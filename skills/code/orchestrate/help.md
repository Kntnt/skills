# orchestrate

## NAME

orchestrate - work ready-for-agent tickets in dependency waves

## SYNOPSIS

**/orchestrate** [**--dry-run**] [**--at-once=**_COUNT_] [**--model=**_NAME_] [**--deliberation=**_LEVEL_] [**--fast**] [**--approval=**_IDENTITY_] [**--yes**] [*TICKET-OR-SPEC*...] [**--** *INSTRUCTION*]

**/orchestrate reconcile** [**--commit=**_COMMIT_] [**--yes**] *TICKET* [**--** *INSTRUCTION*]

## DESCRIPTION

`orchestrate` works the current repository's open `ready-for-agent` tickets on the current branch. Fresh subagents build and independently verify each ticket; verified work is integrated, recorded, and closed. The Skill never pushes, tags, or releases.

Blocking relations produce dependency waves. Native tracker relations take precedence over `Blocked by` lines. Where the tracker's relation carries at least one edge, the body's `Blocked by` list is read too, and any ticket the body names that the relation does not is a refusal. A closed blocker remains blocking until its Ticket Resolution is done.

A ticket beginning a line with `Builds alone` is a Solo Ticket. It receives the first available wave by itself, and the plan marks it `solo`.

A ticket may declare ordered multi-commit work with `Commit roles: implementation: src/**; evidence: docs/verification/**`. The keyword may be a sentence or heading; under a heading, write one `- role: pattern, pattern` entry per role. Patterns are Git pathspecs. A valid branch contains one or more complete passes, each role exactly once in declaration order and one commit per role; `.kntnt-orchestrate/` may accompany a role and a commit confined there is skipped. Later amendments append complete passes without rewriting earlier commits.

The main session owns planning, triage, integration, and verification judgements. Run it from the most capable model available; those judgements are only as reliable as that model.

Model Selector creates one frozen routing snapshot before claims. Builders and repair roles use decisions from that snapshot; independent verdicts always inherit the main session's exact model and deliberation configuration. Where that snapshot can select nothing — no profile, a rejected profile, no adapter able to express a point, or no safe candidate — every later role is decided from the frozen account itself, the decision Model Selector made restated under the new name, and Model Selector is invoked once per run rather than once per wave.

Where several measured configurations clear the quality floor, the run selects the cheapest of them, and the fastest of them under **--fast**. The objective is frozen with the snapshot and reported with it.

Before any ticket is claimed, the Skill audits ticket text for open decisions in one batch and posts the answers to their tickets. It looks for concretely named gaps, including exact commands whose inputs the repository does not fix, an external service or account with no mutation path or owner, choices phrased as alternatives, and credentials or accounts whose owner is undeclared. With `--yes`, it parks such tickets under `needs-info` instead of guessing, then continues with the rest; uncertain cases proceed and retain the mid-work park as a backstop.

`reconcile` records that a failed, conflicted, or parked attempt was later completed outside Orchestrate. See **/orchestrate reconcile --help**.

## COMMANDS

**reconcile**

Record that a closed, unsuccessfully attempted ticket was completed outside Orchestrate.

## POSITIONAL ARGUMENTS

*TICKET-OR-SPEC*...

Bare references such as `#14`. With no references, the scope is every open ticket carrying `ready-for-agent`. With references, the scope is the union of each named ticket and each named spec's children.

A reference filed as the parent of other tickets is a spec and is never built itself. Where the tracker exposes no parent relation, a `Parent` line in a ticket body is the fallback. A reference that does not resolve, is not a number, or uses `owner/repo#number` makes the complete invocation invalid.

Naming a ticket narrows the scope but does not bypass blockers, claims, readiness checks, or an outcome already recorded on the ticket.

## TICKET EXECUTION

**Claim**

The ticket is assigned before work starts. Another user's or active run's claim is skipped. An interrupted claim from this run can resume when its identity is recoverable.

**Build**

A fresh subagent receives the complete ticket thread, parent spec, Project instructions, verification commands, and isolated workspace data. It receives no private summary.

The verification gate is resolved once at the run's start. Every verifier receives that exact list and neither substitutes nor expands it.

**Verify**

A different subagent checks every acceptance criterion and the complete Project gate without seeing the builder's claims. Delivery requests such as push, pull request, or release are reported but do not change the verdict.

**Integrate**

Verified work is committed and integrated. After each wave, the complete Project gate runs on the combined branch and an independent coherence review reads what that wave merged onto it, the branch before the wave having been read and passed by the check that ended the wave before. A strict subset of failing tests is rerun unchanged three times in isolation; three passes earn one unchanged full-gate rerun, and only a green full rerun turns the result into a pass recorded as a load-induced flake.

Before integration—or at `record` when the ceiling is one—the engine refuses a declared pass that is incomplete, out of order, or touches paths outside its current role. The diagnostic names the commit and offending paths, nothing is merged or recorded, and the ticket tree remains available for inspection.

The verdict turns on whether correction requires a new decision, not on whether every gate command passed. Mechanical findings are fixed by another subagent and checked again until a round is clean.

The fix request names its external checker, reversible work, and available retry. An unresolved choice, an undetermined gate correction, a command still failing after its fix round, or a fix that makes no progress stops the run.

A no-progress fixer on a selected configuration escalates once. A second no-progress round stops the run.

**Close**

The ticket closes only after integration and a passing combined branch. Its outcome names the carrying commit.

## BUILDER STOPS

**Mechanical hinder**

A deterministic environment problem is repaired by the orchestrator and the same brief is attempted once more. If the hinder remains, it follows the failure path.

**Genuine decision**

An ambiguity, missing requirement, or design choice not settled by the ticket parks the ticket under `needs-info`, posts a decision-ready question quoting the ticket's sentence and naming what the ticket must state instead, releases the claim, and records no build outcome. The same record shape applies before claim and mid-work.

The park report includes the ticket's lifetime `amends_spent`, so the remaining budget is known before it is resumed.

**Discovered dependency**

When the missing requirement is carried by another ticket without a done Ticket Resolution, the run writes the missing blocking edge to the tracker, releases the claim, discards the partial isolated build, and offers the ticket again after its blocker has a done Ticket Resolution. This does not consume the ticket's rebuild.

**Failed work**

A stop that is neither mechanical, a genuine decision, nor a discovered dependency enters the same verification-failure path as a failed build.

## FAILURES AND COLLISIONS

A verification failure may receive at most two verifier-informed amends. Each uses a fresh builder and verifier. Failure after the second amend records the ticket failed, with no third amend.

A merge collision is repaired and verified against both tickets. If repair fails, the ticket is rebuilt once from a clean base. A second collision records it as conflicted.

With `--at-once=1`, an unrepaired failure stops later tickets. With concurrency, unrelated isolated tickets continue and dependants become stranded.

## CONTINUING A RUN

Restart an interrupted run with the same invocation and state directory; there is no resume option. Recorded outcomes and numbered amend phases remain settled.

The amendment limit is a per-ticket-lifetime budget. A parked attempt is resumed rather than forfeited: its tracker-backed `amends_spent` survives every park and resume, and subtracting that value from two gives the exact number of further amendments available.

Preserved commits are the mandatory base of a resume, never discarded in favour of a rebuild from scratch. Before dispatch, Orchestrate brings the current run branch into the preserved ticket branch so resolved blockers and other integrated predecessors are present. Uncommitted preserved work waits for a person; an authored collision is repaired on the ticket branch and then judged by the resumed amend's fresh full-ticket verifier.

Prior verdicts remain ticket evidence and the resumed amend receives the immediately preceding verdict verbatim. The report keeps `amends_spent` as the lifetime total and names attempts this invocation inherited under `amends_inherited` and attempts it newly spent under `amends_newly_spent`.

The frozen routing account is not reconstructed from current profile, evidence, price, alias, or Harness state. If it is missing or unreadable while this run still owns a claim, the run stops.

`--model` and `--deliberation` are part of that account. Changing or dropping either is refused. Repeating the same attempt and phase resumes it without spending another attempt.

A current user's claim resumes only when it can be distinguished from another active run. Otherwise the Skill stops.

## OUTCOMES

Every ticket appears once. Report groups tickets by their current Ticket Resolution while retaining Run Outcome and completion provenance.

Run Outcome and Ticket Resolution are different facts. The Run Outcome is the immutable record of one unattended attempt. Ticket Resolution says what the ticket's state is now; a later Reconciliation may change it without rewriting the earlier outcome.

**done**

The work is complete. A reconciled ticket was completed outside Orchestrate; its detail preserves an unsuccessful Run Outcome when one exists, leaves it absent after parking, and does not claim Orchestrate built or independently verified the repair.

**failed**

Verification did not pass. `amends_spent` distinguishes an exhausted two-amend path from work that failed before an available continuation completed. Work remains available for inspection.

**conflicted**

Collision repair and the single rebuild both failed. The report names the ticket and files.

**stranded**

Waiting directly or indirectly on failed work.

**never on the frontier**

Never became workable because of a cycle, external blocker, another claim, stopped integration, or parked decision.

The report names its base commit. A ticket blocked on newly discovered work is reported under its blocker's outcome rather than in a sixth category.

## ROUTED OBSERVATIONS

Orchestrate starts each routed attempt immediately before dispatch, finishes it at an independent verdict or terminal non-model condition, and imports eligible sanitized observations automatically. The final report lists imported, identically skipped, conflicting, and refused identities; ledger refusal never stops the run and requires no user import step. An import that brings a workload cohort to its verified-failure threshold moves that cohort's starting Rung one step up for the next run, and the report names the move, the count behind it, and the one command that restores it.

The report gives each ticket its Time to Verified Pass — the seconds from its first routed launch to its first passing verdict, retries included — beside a status saying which of the four cases it is: `verified_pass` with a number, `not_started` where the run launched no attempt for it, `incomplete` where an attempt has not finished, and `not_passed` where every finished attempt failed, parked, or was blocked.

## OPTIONS

**--dry-run**

Report ticket scope, dependency waves, routing readiness, proposed decisions, and routing capability without claiming or changing tickets.

A dry run mints no run identity, so its preflight can render no Exploration Attempt: a night that starts afterwards may route a role one Rung below what the preview showed, the draw being a fact about a run that did not exist yet.

Routing uses streams and leaves no child process. The repository, home, Codex state and cache, Manager and Skill installations, GitHub, Git state, worktrees, locks, and temporary storage remain unchanged whether the preview succeeds or refuses.

**--at-once=**_COUNT_

Build at most *COUNT* frontier tickets concurrently. The default is `1`; larger values isolate tickets in separate branches and working trees.

**--model=**_NAME_

Lock only the building model dimension for every execution role. Model-selector still selects deliberation from the frozen snapshot. An unavailable, ambiguous, unmappable, or above-main exact model is refused before claims; it never falls through to another model. Verdicts retain exact main-seat inheritance.

**--deliberation=**_LEVEL_

Lock only the building deliberation dimension for every execution role. *LEVEL* is exactly one of `low`, `medium`, `high`, `xhigh`, or `max`; another value is refused rather than normalized. Model-selector still selects model when it is omitted. Verdicts retain exact main-seat inheritance.

**--fast**

Select the fastest configuration that holds quality rather than the cheapest one. The objective is frozen for the whole run alongside `--model` and `--deliberation`, so a resumed invocation that adds or drops it is refused before anything is claimed. It changes nothing about the quality floor: a configuration that does not clear it is not chosen for being quick.

**--approval=**_IDENTITY_

Authorize the first plan of this invocation by its exact canonical identity. The engine compares the supplied and computed identities before routing or claiming, records both with the payload on a real plan, and refuses a mismatch. The first matched payload becomes the authorization ceiling for later unflagged plans. Dry runs emit the identity and payload but store nothing. Omitting this option keeps the ordinary flow.

The payload fields, in order, are `branch, default_branch, scope, at_once, worktrees, model, deliberation, waves, solo`. Serialize that object as UTF-8 JSON with sorted keys, `ensure_ascii=False`, and separators `(',', ':')`. Prefix those bytes with the UTF-8 bytes of `kntnt-orchestrate-plan-v1`, followed by one NUL byte, then take the lowercase hexadecimal SHA-256 digest.

A later unflagged plan stays within the authorization ceiling only while `branch`, `default_branch`, `scope`, `at_once`, `worktrees`, `model`, and `deliberation` remain equal, every planned ticket appeared in the ceiling's waves, and every ceiling Solo Ticket still planned remains Solo. Wave order and membership among remaining tickets may change. Drift leaves the expected identity and ceiling payload intact, records the drifted identity, marks the expectation unmet, and keeps claims closed until a flagged plan exactly matches and installs its payload as the new ceiling.

**--commit=**_COMMIT_

Name the default-branch commit that completed a reconciled ticket. It applies only to `reconcile`; the action discovers the commit when one exact closing-reference candidate exists.

**--yes**

Assume yes for every yes-or-no question. A ticket containing an open choice is parked rather than guessed because the option cannot choose among alternatives.

## FILES

**.git/kntnt-orchestrate/**

Concurrent ticket worktrees, branches, reservations, and scratch space. Successful resources are removed; failed and conflicted resources remain for inspection.

**Per-session state directory**

Stores the recoverable claim account, the caller's expected and computed approval identities, and the irreplaceable frozen routing snapshot. The first matched approval payload is the authorization ceiling for later unflagged plans. A missing routing snapshot or an unmet approval stops a claim.

The directory also contains `kntnt-orchestrate-progress.json`, an atomically replaced dashboard of the current wave, ticket, phase, amendment count, completed and remaining ticket counts, timestamp, and terminal outcome. The `report` verb projects its five outcome lists into the terminal dashboard directly, so the two accounts agree. It may lag a transition whose step did not report it and is never evidence or an input to an engine decision; the durable report remains authoritative. Deleting it harms nothing because the next transition recreates it.

**.kntnt-orchestrate/generated.json**

Declares generated files and their commands. A collision confined to declared files is settled by regenerating them on the merged tree. Any undeclared or unresolved collision takes the repair path.

**Run-owned append files**

Builders leave changes to shared append-only files in ticket-specific notes. The orchestrator applies those notes serially after each wave and verifies the result.

**~/.kntnt/orchestrate/flakes.jsonl**

The Skill-owned append-only ledger records load-induced flakes with their unchanged-head isolation and full-rerun evidence. The final report names this run's flakes and how many earlier records each test has in the same repository.

## DIAGNOSTICS

An invalid reference, option, value, combination, or argument order is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, starts nothing, and points to `/orchestrate --help`.

Routing is refused rather than adjusted. A changed snapshot, mismatched locks, routed verdict, or execution role without a decision starts no work and reports a stable reason code.

A mismatched approval reports the expected identity, computed identity, and canonical payload. A later plan that exceeds a matched ceiling names the first protected field, added ticket, or lost Solo constraint, preserves the ceiling audit, and makes approval unmet. A real mismatch or drift changes neither tracker nor repository; a dry-run mismatch or drift stores nothing.

The working tree must be clean when planning and before closing a ticket. A scope with no workable ticket is reported without starting a build.

## EXAMPLES

**/orchestrate --dry-run**

Print the dependency-wave plan and proposed read-only routing decisions for every open `ready-for-agent` ticket without claiming one.

**/orchestrate --at-once=2 --deliberation=high #14 #21**

Work the union of two ticket or spec references with at most two concurrent builders.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

The following schematic cases pin the split independently of any one Skill's Formal Invocation grammar; `\n\n` denotes two newline characters in one payload.

| Case | Envelope | Formal Invocation | Contextual Instruction | Outcome |
| --- | --- | --- | --- | --- |
| Same line | `/skill --force -- Preserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Blank lines | `/skill --force --\n\nPreserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Empty suffix | `/skill --force --   ` | `/skill --force` | — | Syntax refusal |
| Later separator | `/skill -- Preserve -- deployment facts` | `/skill` | `Preserve -- deployment facts` | Envelope valid; formal grammar next |
| No separator | `/skill Preserve deployment facts` | `/skill Preserve deployment facts` | — | No split; formal grammar decides |
| Attached and quoted | ``/skill --force foo--bar `--` "--"`` | ``/skill --force foo--bar `--` "--"`` | — | No split; formal grammar decides |
| Exact help | `/skill --help -- Explain this page` | `/skill --help` | `Explain this page` | Context refusal; render nothing |

## DEPENDENCIES

**Binaries**

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with write access to the current repository and support issue dependencies and sub-issues.

**Skills**

The Manager and Model Selector Skills must be Enabled so the dependency check can run and Orchestrate can use model-selector's public route Interface.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and starts nothing when it is Unsatisfied.

## SEE ALSO

**/ready-for-agent-check --help**, **/commit --help**, **/release --help**
