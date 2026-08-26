# Kntnt Skills

The domain of distributing, enabling, and updating a collection of Agent Skills across coding harnesses.

## Language

An entry says what a term means and what to call it instead. What is true of a term — what the Manager does with it, what a Skill promises about it — is stated in [`docs/rules/`](docs/rules/), and an entry whose law lives there names the module holding it.

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
A standalone Agent Skill with its own name. Collection skills are not namespaced under `kntnt`. What the collection ships as a Skill is stated in `docs/rules/collection.md`, and the files one carries — its help pages among them — in `docs/rules/skills.md`.
_Avoid_: module, plugin, recipe, command, slash command

**Language Resource**:
The single installed source for one language or locale's editorial guidance. It carries the canonical language code, a bounded set of selector aliases, and separate scopes for composing, reviewing, catching machine-sounding prose, and correcting mechanics; a scope is named for the guidance it holds rather than for the Skill that reads it, and a locale variant may inherit the scopes of its base language. What may be written into one is stated in `skills/kntnt/library/references/languages/README.md`.
_Avoid_: language pack, translation, alias registry

**Source Fidelity**:
The Write Skill's truthful representation of the material supplied for a new text: facts, attribution, uncertainty, scope, chronology, causality, and the meaning of edited interview quotations remain supported by that material. It is not external fact-checking, and it is no other editorial Skill's contract.
_Avoid_: fact-checking, source validation, Redline verification

**Text Artifact**:
One coherent text that Write creates or that Redline or Proofread processes. Write may use several source materials to create one Text Artifact; how many of them one invocation of an editorial Skill may carry is stated in that Skill's own shipped documents.
_Avoid_: document batch, input collection, text payload

**Handoff Metadata**:
Optional metadata carried with a Text Artifact that records the resolved genre, technique, and language. Which editorial Skill writes one and which reads one is stated in their own shipped documents.
_Avoid_: required frontmatter, source brief, invocation cache

**Correction Budget**:
The maximum number of subagent corrections Redline may apply after its initial review. What a budget counts, and what spends none of it, is stated in that Skill's own shipped documents.
_Avoid_: iteration count, review count, retry limit

**Output Target**:
The response or filesystem destination to which a Skill delivers its resulting Text Artifact. It is independent of where the source material came from.
_Avoid_: stdout, output mode, source location

**In-place Editing**:
The user's explicit choice to replace the single writable local file that supplied a Text Artifact instead of delivering the result to another Output Target. Inline text, URLs, and read-only files cannot be edited in place.
_Avoid_: inline editing, automatic overwrite, mutable mode

**User-invoked skill**:
A skill the user starts by typing `/name`. Same gesture in every harness; the body is static instructions, not a preprocessed prompt template.
_Avoid_: command, slash command

**Model-invoked skill**:
A skill the model may load on its own when the task matches the skill's description.

**Invocation Envelope**:
The complete input through which any caller starts exactly one Skill: one Formal Invocation and an optional Contextual Instruction.
_Avoid_: command line, arguments

**Formal Invocation**:
The structured part of an Invocation Envelope that names the Skill and supplies only the command path, positional arguments, and flags its declared grammar accepts. The order it is written in is stated in `docs/rules/skills.md`.
_Avoid_: prompt, context

**Contextual Instruction**:
Optional natural-language guidance that accompanies a Formal Invocation without becoming part of its grammar. It may clarify or narrow choices within the Skill's contract and overrides older conversational preferences within those choices, but cannot contradict or widen the contract and may be omitted when the conversation already carries the needed context.
_Avoid_: brief, prose argument, extra arguments

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
The manager subcommand that refreshes this collection's skills and then checks every Dependency again. What it promises is stated in `docs/rules/collection.md`.
_Avoid_: upgrade, sync, pull

**Uninstall**:
The manager subcommand that takes this collection off this machine: every Catalog skill Enabled in Global, and the Manager itself. What it promises, including why it has no `--project` form, is stated in `docs/rules/collection.md`.
_Avoid_: remove, delete, purge, reset

**Help**:
The Manager subcommand that prints the Manager's own help, or the help for one of its own subcommands. It is not how another Skill's help is reached. What it promises is stated in `docs/rules/collection.md`.
_Avoid_: usage, man

**Assume yes**:
What `--yes` means on any collection skill: no question is asked at all — every question that could be answered yes or no is answered yes instead. What follows from that — how a yes/no question is worded, and where the flag is also the gate — is stated in `docs/rules/collection.md`.
_Avoid_: force, non-interactive, quiet, auto-approve

**Solo Ticket**:
A ticket that shares its wave with no other ticket, declared on a line of its own body opening `Builds alone`. When an author writes that line, and what a scheduler owes a ticket carrying it, are stated in `docs/rules/tickets.md`.
_Avoid_: exclusive ticket, serial ticket, locked wave, blocked by everything

**Frame Record**:
The record a framing writes when it maps a task, and the input the Skill that slices that task into tickets reads. It is one untracked working file in the repository being framed rather than a durable account of decisions, and its seven sections and its lifecycle are stated in `skills/kntnt/library/references/frame-record.md`.
_Avoid_: framing document, plan, spec, brief, design doc

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
A Harness that is present in the layer being acted on: the parent of its skills directory for that layer exists — `~/.claude` for Global, `.claude` in the working directory for Project. In the Project layer a Harness whose skills directory is not hidden is never detected, its name being indistinguishable from the repository's own content. Which verbs act on the set, and what they do where nothing is detected, are stated in `docs/rules/collection.md`.
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

**Capability**:
A Dependency on what the running Harness can do rather than on what is on disk — spawning subagents, for one. No script can test one, because the Manager cannot know which Harness invoked it; the agent answers, being the Harness. How one is reported, and how a skill requiring one behaves where it is Unsatisfied, are stated in `docs/rules/collection.md`.
_Avoid_: feature, harness flag, platform check, gate

**Satisfied**:
A dependency that is present and usable: the skill exists in the harness directory, the binary is on PATH, or the agent confirms the Capability of itself.
_Avoid_: installed, resolved, met

**Unsatisfied**:
A dependency that is missing. What the dependent skill then does is stated in `docs/rules/collection.md`.
_Avoid_: broken, missing (say unsatisfied)
