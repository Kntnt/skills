# Phase 1, step 1 — triage of `docs/adr/` and the rest of the instruction pile

> Recon output for phase 1 of the rebuild. Written 2026-08-25 against commit `c6a757d`. Provisional: the bins below are a proposal, settled with Thomas in step 2. Deleted with the rest of `docs/rework/` by the final cleanup ticket.

## What the pile actually is

96 records, numbered 0001–0106 with ten gaps (0031–0034, 0081, 0082, 0086, 0092, 0100, 0102). 304 KB, ~1 160 physical lines — long single-line paragraphs, not many short files. Nothing in `docs/` is auto-loaded today; `AGENTS.md` routes to it with `read when` lines.

Three findings from the sweep matter more than any individual classification.

**A living rules document already exists, and the convention for keeping it is already written down.** `docs/rules/skills.md` states current law as rules and cites the record for the reasoning instead of repeating it; `docs/rules/general.md` makes that a duty in its *Refactoring completeness* section — *the records carry why and when, this standard carries what is true now*, and a change that moves a record in a rule area binding more than one Skill must state the resulting rule in the standard in the same change. The reform is therefore not the invention of a format. It is the completion of one that covers Skill *form* and stops there.

**`CONTEXT.md` is a second rules document wearing a glossary's clothes.** Its entries for Select, Update, Uninstall, Assume yes, Digest, Deviating, Withdrawn, Catalog, Partial, Detected Harness and Capability are normative specifications several paragraphs long, not definitions. That is where the Manager's behavioural law actually lives today. Anyone answering *what applies now* has three places to look, and the records are only one of them.

**A large share of the pile is why-documents for rules the shipped files already state.** The clearest case is `agents-md`: ADR-0016, 0017, 0019, 0020, 0021, 0022, 0023, 0024 and 0025 are cited by no file outside `docs/adr/`, and every rule they settle is stated in that Skill's own `SKILL.md`, `help.md` and `references/placement.md`. `general.md` already says such a rule needs nothing central — *a rule governing one Skill's own behaviour needs nothing here, that Skill's shipped documents being where a reader already meets it*. For these records, deletion loses no rule at all.

## Where else instructions live

| Place | What it holds | Bearing on the reform |
|---|---|---|
| `docs/rules/general.md` | Code form, design philosophy, refactoring completeness, naming, packaging, tooling | Already the rules-doc format. Absorbs, does not compete. |
| `docs/rules/python.md` | Python baseline, PEP 723, tooling | Unaffected. |
| `docs/rules/skills.md` | What a Skill ships: frontmatter, body, grammar, Library, manpages, Codex sidecar, README | Already the rules doc for Skill form. 32 ADR citations point here from it. |
| `CONTEXT.md` | Domain glossary — in practice, the Manager's behavioural spec | Needs a decision: glossary or law. |
| `AGENTS.md` | Ground rules + `read when` References lines | The router. Gets the rules doc's entry. |
| `CONTRIBUTING.md` | The four checks, catalog regeneration, reference-validator comparison | Procedure; unaffected except for ADR links. |
| `docs/evaluation/protocol.md`, `docs/research/*` | Evaluation protocol, manpage research | Unaffected. |
| `skills/kntnt/library/references/editorial/README.md`, `.../languages/README.md` | Format pages for editorial and language resources | Unaffected; already the right shape. |
| Each Skill's own `SKILL.md`, `help.md`, `references/` | That Skill's behaviour | Where a one-Skill rule belongs. Already carries most of them. |
| `tests/test_adr.py` | Numbering uniqueness, citation resolution, outrun pointers in both directions, hand-listed relation pairs | Must be rewritten by the deletion sweep. 562 ADR citations live in `tests/`. |

## Do ADR-0067 and ADR-0099 still bind?

**Both bind, and the rebuild sharpens rather than relaxes them.**

ADR-0067 — *a ticket asserts only what stays true until it is built*: no record numbers, symbols rather than line numbers, quantify rather than enumerate, state the vantage commit. The new pipeline splits the ticket from the plan, and the split is exactly this rule's shape: the durable ticket layer must not rot, while `/compile` produces the excerpts and exact files just-in-time against HEAD, where they cannot drift. So the four rules bind the ticket layer *harder* than they did, and are deliberately lifted at the plan layer. The serial-resource rule survives as machinery rather than convention: `/compile` pre-allocates ADR and migration numbers from one shared counter per batch, which is what ADR-0071 already did at run time.

ADR-0099 — *a ticket that rewrites an invariant declares that it builds alone*: the brief rescues the Solo Ticket concept explicitly, and `/dispatch` recomputes waves at runtime, so the declaration is read by the scheduler exactly as before. Binding, unchanged.

Both are `AGENTS.md` References lines today, and their rules belong in the rules doc so a ticket author meets them without opening two records.

## The bins

Each record is classified twice, because the brief's four bins conflate two independent questions.

**Record** — what happens to the file: `DROP` (deleted; git remembers), `C1`–`C6` (folded into a named consolidation record), `KEEP` (stays standalone).

**Rule lands in** — where the still-binding rule is stated afterwards: a rules-doc module, an existing standard module, that Skill's own shipped files, or `—` where nothing binding survives.

The brief's *move-to-standard* bin is the row where the record drops and the rule lands in an existing standard module; its *rules-doc line* bin is the row where the record drops or folds and the rule lands in a rules-doc module.

**Three rows were corrected after the fact, in #134.** ADR-0008, ADR-0015 and ADR-0029 were recorded here as landing in `skills.md` on the belief that the standard already stated them; it stated none of the three, and #128 wrote all three into `collection.md` instead. The column now says `collection.md` for each, which is where the rule is stated and where it stays: what the collection publishes, what a Category is for, and what a flag promises about the collection's questions are all promises of the collection rather than facts about the files a Skill carries. The `Record` column is untouched — the C2 and C3 sets and their counts are what they were.

Twenty-two records belong to orchestrate's runtime and die with that Skill in phase 3; they are the rows whose justification says so, and `run.py` or the orchestrate tests cite nearly all of them, which is why they outlive phase 1. `†` is a narrower mark inside that class: the twenty-one whose field evidence the `/dispatch` design should cite from git rather than rediscover. ADR-0058 is the twenty-second — orchestrate runtime, cited by `run.py`, but its own premise is already outrun, so there is nothing there to carry forward.

### Proposed consolidation records

- **C1 — The distribution model.** How the collection reaches a machine: transport, layers, detection, Catalog, Digest, and what Select, Update and Uninstall each promise.
- **C2 — The invocation grammar.** The Envelope and its separator, strictness, attached flag values, invocation order, help routing.
- **C3 — What a Skill ships.** Frontmatter, body, resource directories, the Collection Library, manpages, the Codex sidecar, and when a model may start a Skill.
- **C4 — The editorial contract.** Language Resources, the shared base contract and its review half, delivery and in-place editing, the anti-slop catalogue, the evaluation corpus.
- **C5 — Routing and evidence.** Model-selector's public route Interface, frozen snapshots, carried controls, observations, and owned Harness integrations.
- **C6 — How this repository records decisions and writes tickets.** The reform's own record: rules doc versus archive, ticket assertions, Solo Tickets, outrun pointers, the reference validator as a baseline.

### The table

| # | Subject | Record | Rule lands in | Why |
|---|---|---|---|---|
| 0001 | Orchestrate the transport | C1 | `collection.md` | Founding scope decision; the rule is one line, the why is worth carrying. |
| 0002 | Manager subcommands, skills unprefixed | C1 | `collection.md` | Current law; trivial why. |
| 0003 | Disk is truth, apply is idempotent | C1 | `collection.md` | Load-bearing invariant behind Select, Update and integration removal. |
| 0004 | Global default, `--project` override | C1 | `collection.md` | Current law. |
| 0005 | One set per layer, no harness matrix | C1 | `collection.md` | Record says itself it is now trivially true; the why is the reason the matrix never grew. |
| 0006 | Transport installs only the Manager | C1 | `collection.md` | Current law. |
| 0007 | A new Catalog entry is offered | C1 | `collection.md` | Rich why — the consent trade was deliberately overturned; carry it. |
| 0008 | Portable skills, no command files | C3 | `collection.md` | What the collection publishes, so it sits with the rest of how the collection reaches a machine; the why is the portability stance. |
| 0009 | Refuse, do not install | C1 | `collection.md` | Current law, cited from shipped bodies. |
| 0010 | Select, not Setup | DROP | — | Nothing survives that ADR-0035 and ADR-0043 do not state. |
| 0011 | Update re-checks dependencies | C1 | `collection.md` | Current law. |
| 0012 | Skill owns dependencies | C3 | `skills.md` | Already a rule in the standard; the record is its citation. |
| 0013 | A Project cannot hide a Global skill | C1 | `collection.md` | Current law with a real rejected alternative. |
| 0014 | Setup records the harness list | DROP | — | Marked **Retired** in its own first line. |
| 0015 | Skills grouped by category | C3 | `collection.md` | A Category is visible only in Select's list, so the rule sits with the verb; identity is the name, not the path. |
| 0016 | `docs/` versus `agents.d/` | DROP | agents-md's own files | Stated in `references/placement.md`; cited nowhere outside `docs/adr/`. |
| 0017 | `CLAUDE.md` is a one-line bridge | DROP | agents-md's own files | Same; half of it is already superseded by ADR-0019. |
| 0018 | `agents-md` is model-invoked with safe writes | C3 | `skills.md` | The model-invocation half generalised into ADR-0094; the write set is the Skill's own. |
| 0019 | The description is the only hook | C3 | `skills.md` | Already a rule in the standard's frontmatter section. |
| 0020 | Ground rules when narrative docs exist | DROP | agents-md's own files | Stated in the Skill; cited nowhere else. |
| 0021 | One concern per `agents.d/` file | DROP | agents-md's own files | Same. |
| 0022 | No facts means no files | DROP | agents-md's own files | Same. |
| 0023 | `--force` lays the skeleton | DROP | agents-md's own files | Same; a flag's behaviour, not a decision. |
| 0024 | Strip only for tracked Project skills | DROP | agents-md's own files | Same. |
| 0025 | References lines say `read when` | DROP | `docs.md` | An instruction, not a decision — and this repository's own `AGENTS.md` is written to it. |
| 0026 | Delegation's user scope is per-harness | DROP | delegation's own files | One Skill's scope behaviour; the why is a harness fact, not a trade-off. |
| 0027 | Bare `/kntnt` is Help | C1 | `collection.md` | Record says itself it is now trivially true. |
| 0028 | Update re-adds what deviates | C1 | `collection.md` | The transport-defect why is worth keeping; the rule is one line. |
| 0029 | `--yes` means assume yes everywhere | C2 | `collection.md` | Two clauses already withdrawn by ADR-0059; what survives is a promise about the collection's questions and its deletion gates, stated with the verbs that ask them. |
| 0030 | A harness Capability is a Dependency | C1 | `collection.md` | Current law, cited from shipped bodies. |
| 0035 | Targets are detected, never recorded | C1 | `collection.md` | Current law with a strong rejected alternative. |
| 0036 | A change is reported from the disk | C1 | `collection.md` | Current law; the issue-7 evidence is the why. |
| 0037 | A withdrawn skill is removed without asking | C1 | `collection.md` | Current law; the consent asymmetry with ADR-0007 is the why. |
| 0038 | `--project` selects a layer | C1 | `collection.md` | Current law; mostly restates ADR-0013 and ADR-0043. |
| 0039 | The Catalog is fetched; only Update stores it | C1 | `collection.md` | Current law; the diff dependency is the why. |
| 0040 | Uninstall clears the machine, not the Project | C1 | `collection.md` | Current law. |
| 0041 | The Digest answers freshness | C1 | `collection.md` | Current law; *Deviating*, not *out of date*, is a vocabulary rule. |
| 0042 | `--dry-run` is a real run in a Sandbox | C1 | `collection.md` | Current law; the measured `HOME` fact is the why. |
| 0043 | Select is one verb in place of three | C1 | `collection.md` | Current law; the *reading is not side-effecting* rule matters. |
| 0044 | Help lives with the skill | C2 | `skills.md` | Already a rule in the standard; amended by ADR-0077. |
| 0045 | The agent is the renderer | C1 | `collection.md` | Current law; the measured no-TTY evidence is worth keeping. |
| 0046 | The body carries only what the agent executes | C3 | `skills.md` | Already a rule; its own count claim is already outrun. |
| 0047 | Dependencies resolved before anything is written | C1 | `collection.md` | Current law. |
| 0048 | TL;DR mode is a standing instruction | DROP | tldr's own files | Its grammar half is withdrawn by ADR-0103 and its output half superseded by ADR-0080; the mechanism is the Skill's own. |
| 0049 | Unconditional when asked, gated when standing | DROP | — | Superseded outright by ADR-0080. |
| 0050 | All deterministic reasoning behind one seam | DROP † | — | The `run.py` engine is being deleted; the rebuild's stated goal is no script runtime at all. |
| 0051 | The tracker remembers what a run recorded | DROP † | — | Orchestrate runtime; `/land` and the journal replace it. |
| 0052 | The invocation is the resume | DROP † | — | Orchestrate runtime; the rule survives as `/dispatch`'s resume, which will state it itself. |
| 0053 | A scope narrows the set, never the rules | DROP † | — | Orchestrate runtime; the shared selection grammar replaces it. |
| 0054 | The ceiling carries the isolation decision | DROP † | — | Orchestrate runtime; `/dispatch` always isolates. |
| 0055 | A collision is repaired on the losing branch | DROP † | — | Orchestrate runtime; `/dispatch` re-forks from the fresh tip instead. |
| 0056 | A run refuses a tree it cannot account for | DROP † | — | Orchestrate runtime. |
| 0057 | A working tree belongs to its run branch | DROP † | — | Orchestrate runtime. |
| 0058 | The closed half of a scope is bounded | DROP | — | Orchestrate runtime; its own premise is already outrun by issue #81. |
| 0059 | Unknown subcommand and disallowed flag are errors | C2 | `skills.md` | Current law across every Skill; already stated in the standard. |
| 0060 | Frontmatter is read by a real YAML parser | C3 | `skills.md` | Current law; the cold-start cost is the why. |
| 0061 | One flat, prefixed `metadata` namespace | C3 | `skills.md` | Current law; already stated in the standard. |
| 0062 | `compatibility` states the environment | C3 | `skills.md` | Current law; already stated in the standard. |
| 0063 | On-demand files live under `references/` | C3 | `skills.md` | Current law; already stated in the standard. |
| 0064 | A run works the branch it was left on | DROP † | — | Orchestrate runtime; `/dispatch` lands on the branch it was invoked from by design. |
| 0065 | The requirement is the whole thread | DROP † | — | Orchestrate runtime; `/compile` reads the thread at compile time instead. |
| 0066 | The reference validator is a baseline | C6 | `skills.md` | Current law with a live consequence for every new Skill; the baseline claim needs its record. |
| 0067 | A ticket asserts only what stays true | C6 | `tickets.md` | Binding and sharpened by the split between ticket and plan; the evidence tables are the why. |
| 0068 | An unreadable declaration is not a declaration of nothing | C1 | `collection.md` | Current law at the dependency gate. |
| 0069 | A failed verification buys one amend | DROP † | — | Orchestrate runtime; `/dispatch`'s REVISE/REBUILD verdicts replace it. |
| 0070 | A run asks at plan time or not at all | DROP † | — | Orchestrate runtime; `/compile`'s `needs-info` parking replaces it, earlier and cheaper. |
| 0071 | What parallel tickets share, the run allocates | DROP † | — | Orchestrate runtime; `/compile` pre-allocates and `/dispatch` owns the append files. |
| 0072 | The wave check reads coherence | DROP † | — | Orchestrate runtime; the dispatcher's review and the per-merge gate replace it. |
| 0073 | A discovered edge corrects the graph | DROP † | — | Orchestrate runtime; already partly superseded by ADR-0079. |
| 0074 | Building is delegated down, the verdict never | DROP † | — | Orchestrate runtime; superseded by ADR-0085 and re-decided in the delegation doctrine. |
| 0075 | A later record leaves a pointer in the earlier one | C6 | `docs.md` | The discipline the archive needs; its cost is what the reform is removing. |
| 0076 | Shared implementation belongs to the Library | C3 | `skills.md` | Current law; already stated in the standard. |
| 0077 | Subcommands have addressable manpages | C2 | `skills.md` | Current law; already stated in the standard. |
| 0078 | The Invocation Envelope | C2 | `skills.md` | Current law across every Skill; already stated in the standard. |
| 0079 | Run Outcome is history, Ticket Resolution is current | DROP † | — | Orchestrate runtime; `/land` absorbs Reconciliation. |
| 0080 | TL;DR selects for the owner of the outcome | KEEP | tldr's own files | The register every new Skill adopts by reference; the perspective argument is not restatable in one line. |
| 0083 | Model-selector owns exact frozen routing | C5 | `collection.md` | Current law; `/dispatch` routes through this Interface. |
| 0084 | A fresh amended verdict buys one continuation | DROP † | — | Orchestrate runtime. |
| 0085 | Orchestrate routes execution, inherits verdicts | DROP † | `collection.md` | The Skill dies; the *verdicts inherit the main seat* rule survives in the delegation doctrine. |
| 0087 | A Language Resource co-locates selectors and scopes | C4 | `skills.md` | Current law for the editorial Skills. |
| 0088 | Editorial Skills compose without Write provenance | C4 | `skills.md` | Current law. |
| 0089 | Routed work reports the evidence it never imports | C5 | `collection.md` | Current law; `/dispatch` inherits the emission contract. |
| 0090 | A Skill owns the integrations it installs | C5 | `skills.md` | Current law; already stated in the standard's `kntnt.integrations` rule. |
| 0091 | Delivery is the response by default | C4 | `skills.md` | Current law for every Skill producing a Text Artifact. |
| 0093 | One corpus, evaluated per provider family | C4 | `docs.md` | Current law; `docs/evaluation/protocol.md` is where a reader meets it. |
| 0094 | A model starts a Skill only inside a bounded description | C3 | `skills.md` | Current law; already stated in the standard. |
| 0095 | A first draft's requirements are stated once | C4 | `skills.md` | Current law; already stated in the standard's Library section. |
| 0096 | A valued flag attaches its value with `=` | C2 | `skills.md` | Current law; already stated in the standard. |
| 0097 | One invocation order | C2 | `skills.md` | Current law; already stated in the standard. |
| 0098 | A fully determined fix is mechanical | DROP † | — | Orchestrate runtime; the constructive-obligation idea is worth carrying into `/dispatch`'s review. |
| 0099 | A ticket that rewrites an invariant builds alone | C6 | `tickets.md` | Binding; the Solo Ticket is rescued into `/dispatch`'s scheduler. |
| 0101 | An adapted catalogue is owned, not depended on | C4 | `skills.md` | Current law; the licence notice rule has a real consequence. |
| 0103 | `/tldr` addresses its mode through a command path | DROP | tldr's own files | One Skill's grammar; the general rule is ADR-0097's. |
| 0104 | A control carried by inheritance completes the point | C5 | — | Model-selector internals; the rule is the adapter schema's, stated in that Skill. |
| 0105 | The valued-flag registry derives from declarations | C2 | `skills.md` | A test's construction rather than a decision; the rule is one line in the standard. |
| 0106 | A collision in generated files is regenerated | DROP † | — | Orchestrate runtime; `.kntnt-orchestrate/generated.json` goes with it. |

### Counts

| Bin | Records |
|---|---|
| `DROP` — orchestrate runtime (dies with the Skill in phase 3) | 22 |
| `DROP` — rules already in the Skill's own files, or already superseded | 14 |
| `C1` — the distribution model | 25 |
| `C2` — the invocation grammar | 8 |
| `C3` — what a Skill ships | 12 |
| `C4` — the editorial contract | 6 |
| `C5` — routing and evidence | 4 |
| `C6` — decisions and tickets | 4 |
| `KEEP` | 1 |
| **Total** | **96 → 29 after phase 1, → 7 once orchestrate goes** |

## Consequences the reform has to carry

**The suite.** `tests/test_adr.py` holds numbering uniqueness, citation resolution and outrun pointers in both directions, with five hand-written relation-pair tests naming specific records. 562 ADR citations sit under `tests/`. Every one of those tests is about a pile that will not exist in this shape; the deletion sweep rewrites the module rather than patching it, and the outrun-pointer machinery has nothing left to hold once records stop narrowing each other.

**`CONTEXT.md`.** Five glossary entries — Run Outcome, Ticket Resolution, Solo Ticket, Reconciliation, Declared Generated File — belong to orchestrate and go with it, except Solo Ticket, which the new scheduler keeps. The larger question is whether the Manager entries stay normative or hand their law to the rules doc and shrink to definitions.

**`AGENTS.md`.** Two of its References lines point at individual records (0067, 0099). Both become rules-doc lines, so the pointers collapse into one.

**`CONTRIBUTING.md`** links ADR-0066 and ADR-0106; the second goes with orchestrate.

**Numbering.** If consolidation records are written into the existing sequence they take 0107 onward and the archive keeps its gaps; if the archive is re-cut, every citation in every shipped file moves at once. Recommendation is the former — a number is an address, and readdressing 232 in-record and 66 in-Skill citations buys tidiness and nothing else.
