# Kntnt Skills

The domain of distributing, enabling, and updating a collection of Agent Skills across coding harnesses.

## Language

An entry says what a term means and what to call it instead. What is true of a term — what a Manager verb does with it, what a Skill promises about it — is stated in [`docs/rules/`](docs/rules/) or in the shipped documents of the Skill it belongs to, and an entry whose law lives in a rules module names that module in one clause.

**Collection**:
The set of skills, shared scripts, and shared documents shipped from the `kntnt/skills` repository.
_Avoid_: package, plugin, marketplace, bundle

**Collection Library**:
The shared references and scripts shipped inside the Manager and available to every Collection Skill. It is not a Skill, a Catalog entry, or something the user Enables separately.
_Avoid_: shared skill, utility skill, support skill

**Category**:
A folder under `skills/` in the collection repository that groups related skills. It is not part of the skill name and cannot be Enabled as a set; what Select does with a Category is stated in `docs/rules/collection.md`.
_Avoid_: namespace, group, tag, section

**Skill**:
A standalone Agent Skill with its own name, never namespaced under `kntnt`. What the collection ships as a Skill, and the files one carries — its help pages among them — are stated in `docs/rules/collection.md` and `docs/rules/skills.md`.
_Avoid_: module, plugin, recipe, command, slash command

**Language Resource**:
The single installed source for one language or locale's editorial guidance. It carries the canonical language code, a bounded set of selector aliases, and separate scopes for composing, reviewing, catching machine-sounding prose, and correcting mechanics; a scope is named for the guidance it holds rather than for the Skill that reads it, and a locale variant may inherit the scopes of its base language. What may be written into one is stated in `skills/kntnt/library/references/languages/README.md`.
_Avoid_: language pack, translation, alias registry

**Source Fidelity**:
The Write Skill's truthful representation of the material supplied for a new text: facts, attribution, uncertainty, scope, chronology, causality, and the meaning of edited interview quotations remain supported by that material. It is not external fact-checking, and it is no other editorial Skill's contract.
_Avoid_: fact-checking, source validation, Redline verification

**Text Artifact**:
One coherent text that Write creates or that an editorial Skill processes. Write may use several source materials to create one Text Artifact; how many of them one invocation of an editorial Skill carries is stated in that Skill's own shipped documents.
_Avoid_: document batch, input collection, text payload

**Handoff Metadata**:
Optional metadata carried with a Text Artifact that records the resolved genre, technique, and language. Which editorial Skill writes one, which reads one, and what happens where it is absent are stated in their own shipped documents.
_Avoid_: required frontmatter, source brief, invocation cache

**Correction Budget**:
The maximum number of subagent corrections a correcting Skill may apply after its initial review. What spends the budget, and what stops the loop before it is spent, are stated in that Skill's own shipped documents.
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
_Avoid_: automatic skill, auto-triggered skill, agent-invoked skill

**Invocation Envelope**:
The complete input through which any caller starts exactly one Skill: one Formal Invocation and an optional Contextual Instruction.
_Avoid_: command line, arguments

**Formal Invocation**:
The structured part of an Invocation Envelope that names the Skill and supplies only the command path, positional arguments, and flags its declared grammar accepts. The order it is written in is stated in `docs/rules/skills.md`.
_Avoid_: prompt, context

**Contextual Instruction**:
Optional natural-language guidance that accompanies a Formal Invocation without becoming part of its grammar. It may clarify or narrow choices within the Skill's contract and overrides older conversational preferences within those choices, but cannot contradict or widen the contract and may be omitted when the conversation already carries the needed context.
_Avoid_: prose argument, extra arguments

**Conversation Context**:
The surrounding session material available to the agent independently of the current Invocation Envelope. Applicable guidance may inform Skill execution under the same contract boundaries as a Contextual Instruction without becoming part of either the Formal Invocation or the Contextual Instruction.
_Avoid_: trailing arguments, implicit instruction

**Manager**:
The always-enabled skill named `kntnt`. It is the collection's only namespaced entry point, and what its verbs promise is stated in `docs/rules/collection.md`.
_Avoid_: installer, CLI, wrapper

**Select**:
The manager subcommand that shows what the collection has and changes it in the same gesture. What it promises is stated in `docs/rules/collection.md`.
_Avoid_: status, enable, disable, picker, menu, add, remove, activate, install

**Update**:
The manager subcommand that refreshes this collection's skills and then checks every Dependency again. What it promises, including what authorizes a real Global run of it, is stated in `docs/rules/collection.md`.
_Avoid_: upgrade, sync, pull

**Uninstall**:
The manager subcommand that takes this collection off this machine: every Catalog skill Enabled in Global, and the Manager itself. What it promises, including why it has no `--project` form, is stated in `docs/rules/collection.md`.
_Avoid_: remove, delete, purge, reset

**Help**:
The Manager subcommand that prints the Manager's own help, or the help for one of its own subcommands. It is not how another Skill's help is reached; what it promises is stated in `docs/rules/collection.md`.
_Avoid_: usage, man

**Assume yes**:
What `--yes` means on any collection skill: no question is asked at all — every question that could be answered yes or no is answered yes instead. What follows from that — how a yes/no question is worded, and where the flag is also the gate — is stated in `docs/rules/collection.md`.
_Avoid_: force, non-interactive, quiet, auto-approve

**Run Outcome**:
The immutable historical result of an unattended Orchestrate attempt against a ticket. A later repair does not change what that attempt did.
_Avoid_: current outcome, ticket status

**Ticket Resolution**:
The current account of whether the work requested by a ticket is complete. How Orchestrate reports it beside an earlier Run Outcome is stated in that Skill's own shipped documents.
_Avoid_: run outcome, tracker state

**Solo Ticket**:
A ticket that shares its wave with no other ticket, declared on a line of its own body opening `Builds alone`. When an author writes that line, and what a scheduler owes a ticket carrying it, are stated in `docs/rules/tickets.md`.
_Avoid_: exclusive ticket, serial ticket, locked wave, blocked by everything

**Reconciliation**:
An explicit maintainer acknowledgement that a ticket with an unsuccessful Run Outcome was completed outside Orchestrate and now has a done Ticket Resolution. It preserves the unsuccessful Run Outcome as provenance.
_Avoid_: retry, overwrite, superseding outcome

**Declared Generated File**:
A file a repository states is the output of a command rather than of a decision, named together with that command in `.kntnt-orchestrate/generated.json`. What an Orchestrate collision confined to such files takes instead of collision repair is stated in that Skill's own shipped documents.
_Avoid_: build artifact, derived file, generated output

**Defect Class**:
The rule a verdict's finding is one instance of, named by the verifier on the line beside the finding. What a verifier owes it and what an amender owes it are stated in Orchestrate's own shipped documents.
_Avoid_: defect category, root cause, finding type, symptom, distillate

**Seat**:
One model running at one exact configuration (model, deliberation, channel, surface) in one role of a run.
_Avoid_: agent, worker, instance, model slot

**Main Seat**:
The Seat the user chose for their own session. What a routed Seat may never exceed, and what is never routed away from it, are stated in `docs/rules/routing.md`.
_Avoid_: parent model, orchestrator model, default model

**Cohort**:
The set of routed attempts that share a role and a kind of work, within which evidence is comparable and a Standing Policy acts. What is never compared across Cohorts is stated in `docs/rules/routing.md`.
_Avoid_: category, bucket, task type, benchmark

**Standing Policy**:
A per-Cohort rule kept as script-owned state beside the user's configuration, with shipped defaults. What it fixes, what moves it, and what it bounds are stated in `docs/rules/routing.md`.
_Avoid_: escalation rule, tier policy, auto-scaling, preset

**Rung**:
One adjacent step on the ladder a Cohort climbs. What that step is in each of its two dimensions is stated in `docs/rules/routing.md`.
_Avoid_: tier, level, size, upgrade, model step

**Outcome Authority**:
What judged a routed attempt from outside it: an independent verifier, an objective checker, a declared failure signal, a frozen rubric, or the user. What an attempt nothing judged is worth is stated in `docs/rules/routing.md`.
_Avoid_: self-report, confidence, status, result

**Time to Verified Pass**:
The wall-clock time from a ticket's first routed attempt to the verdict that passed it, retries included. Where it stands in the order routing decides by is stated in `docs/rules/routing.md`.
_Avoid_: latency, duration, response time, speed

**Exploration Attempt**:
A routed attempt deliberately placed one Rung below its Cohort's current rung to gain contrast. What it is drawn from, and what its outcome may never count against, are stated in `docs/rules/routing.md`.
_Avoid_: experiment, probe, gamble, A/B test

**Usage Record**:
What one finished session on one Seat cost and how long it took. What it carries, and what it may never become, are stated in `docs/rules/routing.md`.
_Avoid_: run observation, evidence, telemetry, metric

**Enabled**:
A skill present on disk in a layer, in each Detected Harness's skills directory for that layer.
_Avoid_: active, installed, on, turned on (installed is what the transport does; enabled is the user's choice)

**Disabled**:
A skill that is not present on disk in that layer.
_Avoid_: inactive, off, uninstalled

**Partial**:
A fact about the disk: a skill's files are present in some of the layer's Detected Harnesses and missing from others. It is not a third state a user chooses — a skill is Enabled or Disabled. What Select shows for such a skill is stated in `docs/rules/collection.md`.
_Avoid_: partially enabled, half-installed, third state, partial state

**Catalog**:
The collection's declared list of its skills, their dependencies, and each skill's Digest, authored in the repository and read from it at every invocation, so that it names what the collection provides now. A copy of it is stored beside the Manager. What a verb does with either — the fallback, and which verb may replace the stored copy — is stated in `docs/rules/collection.md`.
_Avoid_: manifest, registry, index, lockfile

**Digest**:
A content digest of a skill's directory as the collection ships it, computed over sorted relative paths and file contents, and carried by that skill's Catalog entry. The same computation over what is on disk answers the one freshness question the manager can answer honestly — are these the same files. When it is generated and what it ignores are stated in `docs/rules/collection.md`.
_Avoid_: version, revision, release number, hash of SKILL.md

**Deviating**:
What a skill is when its files differ from the Digest the Catalog carries: a truncated install, a hand edit, or a Project copy that has fallen behind. Never *out of date* — the comparison sees two states and no history, so the manager cannot establish direction, and outside a lagging copy the commonest cause is the user's own edit. What is refreshed on the strength of it is stated in `docs/rules/collection.md`.
_Avoid_: out of date, stale, outdated, modified, dirty

**Withdrawn**:
A skill the collection no longer ships: it has left the repository, and with it the Catalog. The Manager is never one, being no Catalog entry. How one is recognized on disk and what Update does with it are stated in `docs/rules/collection.md`.
_Avoid_: deprecated, retired, obsolete, orphaned

**State**:
The user's remembered choices: which skills are Enabled in Global and in each Project. Reconstructable from disk; never the source of truth. Nothing about where skills go is remembered — that is resolved on each run.
_Avoid_: lockfile, config, preferences

**Detected Harness**:
A Harness that is present in the layer being acted on: the parent of its skills directory for that layer exists — `~/.claude` for Global, `.claude` in the working directory for Project. Which verbs act on the set, when it is resolved, and what a Project layer never detects are stated in `docs/rules/collection.md`.
_Avoid_: harness list, agent list, setup file

**Global**:
The desired set that applies on this machine. Which verbs reach it is stated in `docs/rules/collection.md`.
_Avoid_: user, machine, default (say global)

**Project**:
A working directory with its own extra desired set. Which verbs reach it, and what they may and may not do to it, are stated in `docs/rules/collection.md`.
_Avoid_: repo, workspace, local

**Harness**:
A coding agent that loads Agent Skills from a well-known directory (Claude Code, OpenCode, Codex, and others).
_Avoid_: agent, IDE, tool, client

**Transport**:
The existing `npx skills` CLI, used to add, remove, and refresh skill files in harness directories.
_Avoid_: installer, package manager

**Sandbox**:
The temporary home a changing verb runs against under `--dry-run`, and discards afterwards. The verb executes for real against it, so what comes back is an outcome and not a description of intent. What it is seeded with, and what a dry run therefore costs, are stated in `docs/rules/collection.md`.
_Avoid_: preview, simulation, plan, mock, staging

**Dependency**:
A skill or runtime that another collection skill cannot work without. Which party answers each kind of one is stated in `docs/rules/collection.md`.
_Avoid_: requirement, prerequisite

**External**:
A dependency whose source is another collection, not this one.
_Avoid_: third-party, upstream, peer

**Capability Rank**:
The number a Rung is read on: one model's score on the single benchmark that covers most of the candidates a request reaches. Where that number is taken from, and what never becomes one, are stated in `docs/rules/routing.md`.
_Avoid_: quality score, capability (that is the Dependency below), tier, strength

**Capability**:
A Dependency on what the running Harness can do rather than on what is on disk — spawning subagents, for one. No script can test one, because the Manager cannot know which Harness invoked it; the agent answers, being the Harness. How one is reported, and how a skill requiring one behaves where it is Unsatisfied, are stated in `docs/rules/collection.md`.
_Avoid_: feature, harness flag, platform check, gate

**Satisfied**:
A dependency that is present and usable: the skill exists in the harness directory, the binary is on PATH, or the agent confirms the Capability of itself.
_Avoid_: installed, resolved, met

**Unsatisfied**:
A dependency that is missing. What the dependent skill then does is stated in `docs/rules/collection.md`.
_Avoid_: broken, missing (say unsatisfied)
