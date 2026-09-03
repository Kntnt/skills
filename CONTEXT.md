# Kntnt Skills

The domain of distributing, enabling, and updating a collection of Agent Skills across coding harnesses.

## Language

**Collection**:
The set of skills, shared scripts, and shared documents shipped from the `kntnt/skills` repository.
_Avoid_: package, plugin, marketplace, bundle

**Collection Library**:
The shared references and scripts shipped inside the Manager and available to every Collection Skill. It is not a Skill, a Catalog entry, or something the user Enables separately.
_Avoid_: shared skill, utility skill, support skill

**Category**:
A folder under `skills/` in the collection repository that groups related skills. Select lists skills by Category, so related skills are read together. A Category is not part of the skill name and cannot be Enabled as a set.
_Avoid_: namespace, group, tag, section

**Skill**:
A standalone Agent Skill with its own name. Collection skills are not namespaced under `kntnt`. The collection ships skills only — never harness `commands/` files. Every collection Skill ships its root help beside it and prints it when invoked with `--help`; a Skill with subcommands also ships and prints the addressed subcommand page for `/<skill> <command-path> --help`.
_Avoid_: module, plugin, recipe, command, slash command

**Language Resource**:
The single installed source for one language or locale's editorial guidance. It carries the canonical language code, a bounded set of selector aliases, and separate scopes for composing, reviewing, catching machine-sounding prose, and correcting mechanics; a scope is named for the guidance it holds rather than for the Skill that reads it, and a locale variant may inherit the scopes of its base language. Generic editorial rules never move into a Language Resource merely because their examples are written in English.
_Avoid_: language pack, translation, alias registry

**Source Fidelity**:
The Write Skill's truthful representation of the material supplied for a new text: facts, attribution, uncertainty, scope, chronology, causality, and the meaning of edited interview quotations remain supported by that material. It is not external fact-checking. Redline does not compare a written text with its source material, and Proofread changes no substantive content.
_Avoid_: fact-checking, source validation, Redline verification

**Text Artifact**:
One coherent text that Write creates or that an editorial Skill processes. Write may use several source materials to create one Text Artifact; every Skill that processes one — Redline, Proofread, Unslop — takes exactly one Text Artifact per invocation.
_Avoid_: document batch, input collection, text payload

**Handoff Metadata**:
Optional metadata carried with a Text Artifact that records the resolved genre, technique, and language. Write may add it and Redline may consume it, but every editorial Skill remains usable when it is absent.
_Avoid_: required frontmatter, source brief, invocation cache

**Correction Budget**:
The maximum number of subagent corrections a correcting Skill may apply after its initial review. A review that verifies a correction and Redline's final Proofread pass spend none of the budget, and the loop stops early when no findings remain. Redline and Unslop carry the same contract; only what they review against differs.
_Avoid_: iteration count, review count, retry limit

**Output Target**:
The response or filesystem destination to which a Skill delivers its resulting Text Artifact. It is independent of where the source material came from.
_Avoid_: stdout, output mode, source location

**In-place Editing**:
The user's explicit choice to replace the single writable local file that supplied a Text Artifact instead of delivering the result to another Output Target. Inline text, URLs, and read-only files cannot be edited in place.
_Avoid_: inline editing, automatic overwrite, mutable mode

**User-invoked skill**:
A skill the user starts by name: `$name` in Codex and `/name` in Claude. The body is static instructions, not a preprocessed prompt template.
_Avoid_: command, slash command

**Model-invoked skill**:
A skill the model may load on its own when the task matches the skill's description.

**Invocation Envelope**:
The complete input through which any caller starts exactly one Skill: one Formal Invocation and an optional Contextual Instruction.
_Avoid_: command line, arguments

**Formal Invocation**:
The structured part of an Invocation Envelope that names the Skill and supplies only the command path, positional arguments, and flags its declared grammar accepts.
_Avoid_: prompt, context

**Contextual Instruction**:
Optional natural-language guidance that accompanies a Formal Invocation without becoming part of its grammar. It may clarify or narrow choices within the Skill's contract and overrides older conversational preferences within those choices, but cannot contradict or widen the contract and may be omitted when the conversation already carries the needed context.
_Avoid_: prose argument, extra arguments

**Conversation Context**:
The surrounding session material available to the agent independently of the current Invocation Envelope. Applicable guidance may inform Skill execution under the same contract boundaries as a Contextual Instruction without becoming part of either the Formal Invocation or the Contextual Instruction.
_Avoid_: trailing arguments, implicit instruction

**Manager**:
The always-enabled skill named `kntnt`. It is the collection's only namespaced entry point.
_Avoid_: installer, CLI, wrapper

**Select**:
The manager subcommand that shows what the collection has and changes it in the same gesture. It prints the Catalog as a list grouped by Category — one row per skill, carrying a checkbox that is checked when the skill is Enabled in the targeted layer, the skill's one-line description, and any Capability it requires — and the user answers it in one sentence. Checked means Enabled. It targets Global unless `--project` or `--project=on` is given, and it reaches every Detected Harness in that layer. `--on=<skill>` and `--off=<skill>` apply a delta and open no list. `--yes` opens no list either and Enables nothing that was not already Enabled: it refreshes what Deviates and repairs what is incomplete, so an unattended run never places instructions the user has not read. An answer that changes nothing writes nothing. Any row can be read in full before the list is answered: the Skill's own help.md where it is Enabled and the collection's copy of it where it is not, so deciding never requires installing it first. A row whose Dependency is Unsatisfied in that layer is shown locked and names what to check instead, so the structure between Skills is visible before the answer is given. An answer implying more Skills is resolved to its whole closure before anything is written and costs one yes/no question naming exactly the additions, however deep the chain. Unchecking a Skill that a checked one depends on is reported and allowed: the user is told what they left Unsatisfied, not overruled. It replaces Status, Enable, and Disable, which made the everyday change *read a list under one verb, then retype names from it under another*.
_Avoid_: status, enable, disable, picker, menu, add, remove, activate, install

**Update**:
The manager subcommand that refreshes this collection's skills and then checks every Dependency again. It refreshes an Enabled skill whose files Deviate from the Digest and leaves the rest alone, so its report says what moved rather than what was Enabled; it refreshes the Manager every time, the Manager being no Catalog entry and having no Digest to compare. It reports each new Catalog entry and asks whether to Enable it; `--yes` answers yes. It deletes a Withdrawn skill from the layer it is applying, reporting each one and asking nothing. Before a real Global mutation without formal `--yes`, it shows the complete refresh, Enablement, removal, and target-directory plan and waits for a later user response; Contextual Instruction, Conversation Context, earlier guidance, a broad repair request, and an agent-authored handoff provide no authorization. Apply accepts only the approval identity of the exact current plan, and a missing, incomplete, contradictory, or changed identity is refused before the first write. Formal `update --yes` is fresh authorization in its own current Invocation Envelope and remains unattended; a dry run needs none because its mutations stay in the discarded Sandbox. It does not refresh an External. Without `--project` it applies the Global layer; with `--project` it applies the Project layer.
_Avoid_: upgrade, sync, pull

**Uninstall**:
The manager subcommand that takes this collection off this machine: every Catalog skill Enabled in Global, from every Detected Harness, and then the Manager itself, last and through the Transport. It is the only verb with no `--project` form — a Skill in a working directory is checked into that Project and travels with it, so it is never touched and the report says so. `--yes` is its gate.
_Avoid_: remove, delete, purge, reset

**Help**:
The Manager subcommand that prints the Manager's own help, or the help for one of its own subcommands. Bare `/kntnt` means Help, and `/kntnt <command> --help` reaches the same command page directly. It is not how another Skill's help is reached: a Skill one has answers its own `--help` forms, and a Skill one does not have yet is read about in Select, which fetches that help from the collection.
_Avoid_: usage, man

**Assume yes**:
What `--yes` means on any collection skill: no question is asked at all — every question that could be answered yes or no is answered yes instead. Because the flag answers rather than defers, every yes/no question is worded so that *yes* ends it; a question whose yes opens another question has no unattended answer. On a real Global Update, only `--yes` in the current Formal Invocation has this unattended force; inferred, remembered, contextual, or handed-off intent never acquires it, and the internal Apply still receives the exact plan identity. Where a subcommand deletes files the user is choosing to delete, the flag is also the gate — the script refuses without it, because a script cannot prompt. Deleting a Withdrawn skill is not such a choice and is not gated: there is no question to answer, so Update removes it with or without the flag.
_Avoid_: force, non-interactive, quiet, auto-approve

**Run Outcome**:
The immutable historical result of an unattended Orchestrate attempt against a ticket. A later repair does not change what that attempt did.
_Avoid_: current outcome, ticket status

**Ticket Resolution**:
The current account of whether the work requested by a ticket is complete. Report groups tickets by Ticket Resolution while retaining any earlier Run Outcome as provenance.
_Avoid_: run outcome, tracker state

**Solo Ticket**:
A ticket that shares its wave with no other ticket, declared on a line of its own body opening `Builds alone`. An author writes that line where the ticket's subject is a repository-wide invariant — a rule every shipped file is under, which the ticket rewrites or newly enforces — because a blocking edge names a ticket, and what such a ticket excludes is every new instance a concurrent sibling would write. Orchestrate places it in the first wave its blockers admit it in and gives it that wave alone (ADR-0099).
_Avoid_: exclusive ticket, serial ticket, locked wave, blocked by everything

**Reconciliation**:
An explicit maintainer acknowledgement that a ticket with an unsuccessful Run Outcome was completed outside Orchestrate and now has a done Ticket Resolution. It preserves the unsuccessful Run Outcome as provenance.
_Avoid_: retry, overwrite, superseding outcome

**Declared Generated File**:
A file a repository states is the output of a command rather than of a decision, named together with that command in `.kntnt-orchestrate/generated.json`. An Orchestrate collision confined to such files is settled by running those commands on the merged tree and committing the result, with no collision repair; a collision touching any other file is repaired as before. What counts is the declaration, never how a file looks (ADR-0106).
_Avoid_: build artifact, derived file, generated output

**Defect Class**:
The rule a verdict's finding is one instance of, named by the verifier on the line beside the finding. An amender answers the class rather than the instance: it audits every surface the ticket owns for other instances of the same rule and fixes each, so the next fresh verdict cannot fail the ticket on the same rule at a different line. Naming the class is part of the verdict, which travels to the amender whole (ADR-0084), and is never a separate step or a re-judgement (ADR-0074).
_Avoid_: defect category, root cause, finding type, symptom, distillate

**Seat**:
One model running at one exact configuration (model, deliberation, channel, surface) in one role of a run.
_Avoid_: agent, worker, instance, model slot

**Main Seat**:
The Seat the user chose for their own session. It owns every verdict, is the authority ceiling no routed Seat exceeds, and is never selected by the Collection.
_Avoid_: parent model, orchestrator model, default model

**Cohort**:
The set of routed attempts that share a role and a kind of work, within which evidence is comparable and a Standing Policy acts. Evidence never crosses Cohorts as numeric input.
_Avoid_: category, bucket, task type, benchmark

**Standing Policy**:
A per-Cohort rule kept in the user's configuration with shipped defaults. It fixes the Rung a Cohort starts at, moves that Rung one step up after repeated externally verified failures, never moves it down by itself, and bounds Exploration Attempts.
_Avoid_: escalation rule, tier policy, auto-scaling, preset

**Rung**:
One adjacent step on the ladder a Cohort climbs: the next deliberation level on the same model, and, where deliberation is exhausted or not controllable, the next model up by capability regardless of provider.
_Avoid_: tier, level, size, upgrade, model step

**Outcome Authority**:
What judged a routed attempt from outside it: an independent verifier, an objective checker, a declared failure signal, a frozen rubric, or the user. Work never grades itself, and only a judged attempt is evidence.
_Avoid_: self-report, confidence, status, result

**Time to Verified Pass**:
The wall-clock time from a ticket's first routed attempt to the verdict that passed it, retries included. Routing minimises cost first and uses it to decide between configurations that tie on cost; a run started with `--fast` reverses that order.
_Avoid_: latency, duration, response time, speed

**Exploration Attempt**:
A routed attempt deliberately placed one Rung below its Cohort's current rung to gain contrast, drawn from a budget and tagged so its outcome never counts against the production configuration.
_Avoid_: experiment, probe, gamble, A/B test

**Usage Record**:
What one finished session on one Seat cost and how long it took, carrying no outcome and entering no frontier or quality figure.
_Avoid_: run observation, evidence, telemetry, metric

**Enabled**:
A skill present on disk in a layer, in each Detected Harness's skills directory for that layer.
_Avoid_: active, installed, on, turned on (installed is what the transport does; enabled is the user's choice)

**Disabled**:
A skill that is not present on disk in that layer.
_Avoid_: inactive, off, uninstalled

**Partial**:
A fact about the disk: a skill's files are present in some of the layer's Detected Harnesses and missing from others. It is not a third state a user chooses — a skill is Enabled or Disabled — so nothing sets it, nothing stores it, and no answer of the user's can select it. Select shows such a skill checked and marks it incomplete, and confirming the list repairs it.
_Avoid_: partially enabled, half-installed, third state, partial state

**Catalog**:
The collection's declared list of its skills, their dependencies, and each skill's Digest, authored in the repository and read from it at every invocation, so that it names what the collection provides now. A copy is stored beside the Manager and is what a verb falls back to when the origin cannot be reached; a verb that falls back says so. Only Update replaces that copy — a Catalog fetched by a verb that reports rather than changes is reasoned from and not written, or the difference Update reports new and Withdrawn skills from would be gone before it looked.
_Avoid_: manifest, registry, index, lockfile

**Digest**:
A content digest of a skill's directory as the collection ships it, computed over sorted relative paths and file contents, and carried by that skill's Catalog entry. It is generated when the Catalog is generated, so no release depends on remembering to bump anything and no version number is introduced. The same computation over what is on disk answers the one freshness question the manager can answer honestly — are these the same files. It ignores exactly `__pycache__/` and `*.pyc`, on the producing and the consuming side alike.
_Avoid_: version, revision, release number, hash of SKILL.md

**Deviating**:
What a skill is when its files differ from the Digest the Catalog carries: a truncated install, a hand edit, or a Project copy that has fallen behind. Never *out of date* — the comparison sees two states and no history, so the manager cannot establish direction, and outside a lagging copy the commonest cause is the user's own edit. Update refreshes what Deviates; any offer to re-copy says in the same breath that local changes are overwritten. Nothing Deviates on a Catalog that came from the stored copy: those digests describe the collection as of the last Update.
_Avoid_: out of date, stale, outdated, modified, dirty

**Withdrawn**:
A skill the collection no longer ships: it has left the repository, and with it the Catalog. Update deletes a Withdrawn skill from the layer it applies and does not ask, because nothing can Select or update it any longer. It finds one by asking the disk rather than any stored list: a skill installed from this collection carries `metadata` keys prefixed `kntnt.`, so one that carries any of them and the Catalog does not name is Withdrawn, whatever a local file remembers. The Manager is never one, being no Catalog entry. The mirror of a new Catalog entry, which is reported and offered.
_Avoid_: deprecated, retired, obsolete, orphaned

**State**:
The user's remembered choices: which skills are Enabled in Global and in each Project. Reconstructable from disk; never the source of truth. Nothing about where skills go is remembered — that is resolved on each run.
_Avoid_: lockfile, config, preferences

**Detected Harness**:
A Harness that is present in the layer being acted on: the parent of its skills directory for that layer exists — `~/.claude` for Global, `.claude` in the working directory for Project. Select, Update, and Uninstall act on every Detected Harness, and on the shared `.agents/skills` directory alone when none is detected. Nothing is recorded and nothing is asked; the set is resolved at each invocation, so a Harness installed later is reached by the next run. In the Project layer a Harness whose skills directory is not hidden is never detected, its name being indistinguishable from the repository's own content.
_Avoid_: harness list, agent list, setup file

**Global**:
The desired set that applies on this machine. Select and Update without `--project` change only this layer, and Uninstall clears it.
_Avoid_: user, machine, default (say global)

**Project**:
A working directory with its own extra desired set. Select and Update with `--project` change only this layer. They do not change Global. `select --project` cannot uncheck a skill that is Enabled only in Global — this layer holds no copy of it to remove, and there is no subtractive overlay — so the row says the skill is already Enabled in Global instead, which is also how the user avoids Enabling a second copy. Uninstall never reaches this layer at all.
_Avoid_: repo, workspace, local

**Harness**:
A coding agent that loads Agent Skills from a well-known directory (Claude Code, OpenCode, Codex, and others).
_Avoid_: agent, IDE, tool, client

**Transport**:
The existing `npx skills` CLI, used to add, remove, and refresh skill files in harness directories.
_Avoid_: installer, package manager

**Sandbox**:
The temporary home a changing verb runs against under `--dry-run`, and discards afterwards. The verb executes for real — same code, same Transport, same reading of the disk to report from — so what the user gets back is an outcome and not a description of intent. The Sandbox is seeded with this collection's own files as they are now, so a dry run does not report installing what the user already has, and it has its own npm cache, so the first dry run in a session downloads the Transport afresh and takes longer.
_Avoid_: preview, simulation, plan, mock, staging

**Dependency**:
A skill or runtime that another collection skill cannot work without. A Dependency on a collection Skill is one Select can supply, so Select resolves it to its whole closure and asks before it writes; a binary, an External, and a Capability are not Select's to place, and stay the checker's to answer when the Skill is used.
_Avoid_: requirement, prerequisite

**External**:
A dependency whose source is another collection, not this one.
_Avoid_: third-party, upstream, peer

**Capability**:
A Dependency on what the running Harness can do rather than on what is on disk — spawning subagents, for one. No script can test one, because the Manager cannot know which Harness invoked it; the agent answers, being the Harness. The checker therefore reports the Capabilities a skill requires and the skill's own instructions make answering them part of the check. Select names them on the skill's row, so the user knows before choosing that it may refuse to work where they are. A skill declaring one is still Enabled everywhere; it refuses where the Capability is Unsatisfied.
_Avoid_: feature, harness flag, platform check, gate

**Satisfied**:
A dependency that is present and usable: the skill exists in the harness directory, the binary is on PATH, or the agent confirms the Capability of itself.
_Avoid_: installed, resolved, met

**Unsatisfied**:
A dependency that is missing. The dependent skill does no work; it only tells the user how to satisfy it.
_Avoid_: broken, missing (say unsatisfied)
