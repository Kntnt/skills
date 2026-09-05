# The triage of `docs/adr/`

> The list the archive reform is built from. Written 2026-09-05 against commit `a704b9b`, for issue #262. It is consumed by the tickets that write the rules modules and the six consolidation records, and it is deleted by #272 together with the records it names, because a table naming every record cannot outlive the records it names. Until then every number it names must exist, which `tests/test_adr.py` holds it to.

`docs/adr/` holds 153 records, 904 KB across some 2 100 physical lines, and is read as current law. That is the confusion the rework's phase 1 was built to end: an agent deriving what applies today from a pile of immutable records that outrun each other. The rework triaged the 96 records that existed at the fork in `docs/rework/02-adr-triage.md` on the `rework` branch (`git show rework:docs/rework/02-adr-triage.md`). `main` has since added 57 records that triage never saw, and keeps `/orchestrate`, the Skill the rework meant to delete. This table is `main`'s.

## The bins

Six consolidation bins, restated here in the rework's own words.

- **C1 — The distribution model.** How the collection reaches a machine: transport, layers, detection, Catalog, Digest, and what Select, Update and Uninstall each promise.
- **C2 — The invocation grammar.** The Envelope and its separator, strictness, attached flag values, invocation order, help routing.
- **C3 — What a Skill ships.** Frontmatter, body, resource directories, the Collection Library, manpages, the Codex sidecar, and when a model may start a Skill.
- **C4 — The editorial contract.** Language Resources, the shared base contract and its review half, delivery and in-place editing, the anti-slop catalogue, the evaluation corpus.
- **C5 — Routing and evidence.** Model-selector's public route Interface, frozen snapshots, carried controls, observations, and owned Harness integrations.
- **C6 — How this repository records decisions and writes tickets.** The reform's own record: rules doc versus archive, ticket assertions, Solo Tickets, outrun pointers, the reference validator as a baseline.

Two bins sit beside them, also the rework's.

- **`DROP`** — superseded, dead, or an instruction disguised as a decision. The file goes and git remembers it; whatever still binds is stated in the rules module or in the Skill's own shipped files named in the row.
- **`KEEP`** — a real decision that stands alone. The record is neither folded nor deleted, because what it settles is not restatable as a line of rule anywhere.

And one bin the rework did not need.

- **`RUNTIME`** — a record of `/orchestrate`'s own machinery, which on `main` means one cited by `skills/code/orchestrate/scripts/run.py` or by `tests/test_orchestrate.py`. `/orchestrate` stays on `main` and no rules module restates it, so a `RUNTIME` record is neither consolidated nor dropped by this reform. That citation is the whole of the criterion: a record cited by the Manager's script, by a Library script, or by a model-selector script is not thereby `RUNTIME` — it takes its bin on its content, and #272 repoints the citation, as the rework's own deletion commit did.

## How to read the table

One row per record in `docs/adr/`, every record without exception: its number, its own title, its bin, whether the bin has a rework precedent, the rules module its surviving content goes to where it has one, and a note. The module names are the files under `docs/rules/` — `collection.md`, `skills.md`, `tickets.md`, `docs.md`, and `routing.md` where #264 splits the routing law out — which is `docs/coding-standard/` until #263 renames it.

The **New** column reads three ways. An em dash means the rework binned this record and this table keeps that bin. `new record` means the rework never saw the record and the bin is this ticket's judgement under the criteria above. `new bin` means the rework binned the record otherwise and this table departs; every such row is a `RUNTIME` row, `RUNTIME` being the only bin the rework did not have. The two marked classes are what a reader should read in one pass and correct by hand before #264 and #268 through #271 consume the table. A row the rework binned carries the rework's own note, in its words, with whatever `main` has since added to it appended.

**Where the two rules collide, the citation wins, because the ticket's own construction requires it.** A record the rework binned keeps that bin unless a later `main` record superseded it — but the rework binned twenty-two orchestrate records `DROP` on the premise that the Skill was being deleted, and that premise is exactly what `RUNTIME` exists to correct. So `RUNTIME` is settled first, mechanically, from the two files; every other row is the rework's bin or, for a record the rework never saw, a judgement made under the same criteria. Where a later `main` record has outrun a row, the note names it; no such record moved a row out of its bin.

## What to look at first

**Seven `RUNTIME` rows are not about `/orchestrate`.** ADR-0005, ADR-0029, ADR-0030, ADR-0067, ADR-0083, ADR-0089 and ADR-0099 are the distribution model, the invocation grammar, the routing Interface and the ticket layer; the engine and its suite cite them because `/orchestrate` writes tickets and routes work, not because they are its machinery. The stated criterion claims them anyway, and the consequence is visible downstream: the C6 bin is three records rather than five, ADR-0067 and ADR-0099 no longer being folded into the reform's own record, and #266's `tickets.md` cites two records that stay standing. If the criterion was meant to read *about* `/orchestrate` rather than *cited by* it, these are the seven rows to move, and the C2, C5 and C6 consolidation records grow accordingly.

**Nine orchestrate records are binned `DROP` because nothing cites them.** ADR-0050, ADR-0056, ADR-0057 and ADR-0084 carry the rework's own `DROP`; ADR-0139, ADR-0141, ADR-0142, ADR-0143 and ADR-0144 are the records added on `main` that fall the same way. The `RUNTIME` ground is a citation and it does not reach them, so the rework's bin stands and #272 deletes live law for a Skill that is staying — the parked-ticket resume, the approval ceiling, the flake protocol. Correcting this class means widening `RUNTIME` past the citation, which is a decision this ticket was not given.

**Three rows are judgement calls inside the routing bin.** ADR-0134 and ADR-0135 settle how work is delegated rather than how it is routed, and ADR-0109 settles one Skill's grammar; the first two are binned C5 and the third `DROP`, on the reading that the delegation doctrine is part of the routing chain while the spelling of a Skill's flags is not.

## The table

| # | Title | Bin | New | Rule lands in | Note |
|---|---|---|---|---|---|
| 0001 | Orchestrate the transport; do not replace it | C1 | — | `collection.md` | Founding scope decision; the rule is one line, the why is worth carrying. Outrun on `main` by ADR-0130. |
| 0002 | Manager uses `/kntnt` subcommands; collection skills keep their own names | C1 | — | `collection.md` | Current law; trivial why. |
| 0003 | Disk is the source of truth; apply is idempotent | C1 | — | `collection.md` | Load-bearing invariant behind Select, Update and integration removal. |
| 0004 | Select and Update default to Global; `--project` targets the Project | C1 | — | `collection.md` | Current law. |
| 0005 | One desired set per layer; harnesses are not a matrix | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. The rework binned it C1, and its subject is not /orchestrate's machinery; the citation criterion claims it anyway, which is what makes this one of the seven rows a reader should look at first. |
| 0006 | Transport installs only the manager | C1 | — | `collection.md` | Current law. |
| 0007 | A new Catalog entry is offered, and `--yes` accepts it | C1 | — | `collection.md` | Rich why — the consent trade was deliberately overturned; carry it. |
| 0008 | Portable skills only; no harness command files | C3 | — | `collection.md` | What the collection publishes, so it sits with the rest of how the collection reaches a machine; the why is the portability stance. |
| 0009 | Skills refuse when a dependency is unsatisfied; they never install | C1 | — | `collection.md` | Current law, cited from shipped bodies. |
| 0010 | A skill change is Select, and there is still no Setup | DROP | — | — | Nothing survives that ADR-0035 and ADR-0043 do not state. |
| 0011 | Update re-checks dependencies; it does not refresh externals | C1 | — | `collection.md` | Current law. |
| 0012 | Each skill declares its dependencies; the catalog is generated; checks are shared | C3 | — | `skills.md` | Already a rule in the standard; the record is its citation. |
| 0013 | A Project cannot hide a Global skill | C1 | — | `collection.md` | Current law with a real rejected alternative. |
| 0014 | Setup records the Harness list | DROP | — | — | Marked **Retired** in its own first line. |
| 0015 | The collection repo groups skills by category | C3 | — | `collection.md` | A Category is visible only in Select's list, so the rule sits with the verb; identity is the name, not the path. |
| 0016 | Human docs stay in `docs/`; agent-only files live in `agents.d/` | DROP | — | agents-md's own files | Stated in `references/placement.md`; cited nowhere outside `docs/adr/`. |
| 0017 | CLAUDE.md is a one-line bridge | DROP | — | agents-md's own files | Same; half of it is already superseded by ADR-0019. |
| 0018 | `agents-md` is a Model-invoked skill with a safe write set | C3 | — | `skills.md` | The model-invocation half generalised into ADR-0094; the write set is the Skill's own. |
| 0019 | The `agents-md` description is the only hook | C3 | — | `skills.md` | Already a rule in the standard's frontmatter section. |
| 0020 | Ground rules go in AGENTS.md when narrative docs exist | DROP | — | agents-md's own files | Stated in the Skill; cited nowhere else. |
| 0021 | One concern per file in `agents.d/` | DROP | — | agents-md's own files | Same. |
| 0022 | No facts means no files | DROP | — | agents-md's own files | Same. |
| 0023 | `--force` lays the skeleton; it is not the default | DROP | — | agents-md's own files | Same; a flag's behaviour, not a decision. |
| 0024 | Strip an AGENTS.md line only when a Project skill is the source | DROP | — | agents-md's own files | Same. |
| 0025 | References lines say `read when` the class of work | DROP | — | `docs.md` | An instruction, not a decision — and this repository's own `AGENTS.md` is written to it. |
| 0026 | Delegation's user scope is per-harness; its project scope is not | DROP | — | delegation's own files | One Skill's scope behaviour; the why is a harness fact, not a trade-off. |
| 0027 | Bare `/kntnt` is Help | C1 | — | `collection.md` | Record says itself it is now trivially true. |
| 0028 | Update re-adds what deviates; the transport's `update` is not a refresh | C1 | — | `collection.md` | The transport-defect why is worth keeping; the rule is one line. Outrun on `main` by ADR-0130. |
| 0029 | `--yes` means assume yes, on every skill and every verb | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. The rework binned it C2, and its subject is not /orchestrate's machinery; the citation criterion claims it anyway, which is what makes this one of the seven rows a reader should look at first. Outrun on `main` by ADR-0131. |
| 0030 | A harness requirement is a Dependency the agent answers, not an install-time gate | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. The rework binned it C1, and its subject is not /orchestrate's machinery; the citation criterion claims it anyway, which is what makes this one of the seven rows a reader should look at first. |
| 0035 | Target directories are detected at each invocation, never recorded | C1 | — | `collection.md` | Current law with a strong rejected alternative. |
| 0036 | A change is reported from the disk, never from the plan | C1 | — | `collection.md` | Current law; the issue-7 evidence is the why. Outrun on `main` by ADR-0130. |
| 0037 | A withdrawn skill is removed without asking | C1 | — | `collection.md` | Current law; the consent asymmetry with ADR-0007 is the why. |
| 0038 | `--project` selects a layer, and the Project form shows that layer alone | C1 | — | `collection.md` | Current law; mostly restates ADR-0013 and ADR-0043. |
| 0039 | The Catalog is fetched at every invocation, and only Update stores it | C1 | — | `collection.md` | Current law; the diff dependency is the why. |
| 0040 | Uninstall clears the machine; a Project's copies are the Project's | C1 | — | `collection.md` | Current law. |
| 0041 | The Digest answers freshness, and a mismatch is Deviating | C1 | — | `collection.md` | Current law; *Deviating*, not *out of date*, is a vocabulary rule. Outrun on `main` by ADR-0130. |
| 0042 | `--dry-run` is a real run against a Sandbox that is thrown away | C1 | — | `collection.md` | Current law; the measured `HOME` fact is the why. |
| 0043 | `select` is one verb in place of three | C1 | — | `collection.md` | Current law; the *reading is not side-effecting* rule matters. |
| 0044 | Help lives with the skill, and `--help` is its route | C2 | — | `skills.md` | Already a rule in the standard; amended by ADR-0077. |
| 0045 | The agent is the renderer; no skill may require a terminal | C1 | — | `collection.md` | Current law; the measured no-TTY evidence is worth keeping. |
| 0046 | The skill body carries only what the agent executes | C3 | — | `skills.md` | Already a rule; its own count claim is already outrun. |
| 0047 | Dependencies are resolved before anything is written, and unchecking is reported | C1 | — | `collection.md` | Current law. |
| 0048 | TL;DR mode is a standing instruction, not an output style | DROP | — | brief's own files | Its grammar half is withdrawn by ADR-0103 and its output half superseded by ADR-0080; the mechanism is the Skill's own. The Skill is `brief` since ADR-0113, so the rework's `tldr` landing is renamed here. Outrun on `main` by ADR-0170. |
| 0049 | The template is unconditional when asked for, and gated when standing | DROP | — | — | Superseded outright by ADR-0080. |
| 0050 | All deterministic reasoning lives behind one seam | DROP | — | — | The `run.py` engine is being deleted; the rebuild's stated goal is no script runtime at all. Neither `run.py` nor `tests/test_orchestrate.py` cites it, so the `RUNTIME` ground does not reach it and the rework's bin stands even though the Skill does; the class is ADR-0139's note. |
| 0051 | The tracker remembers what a run recorded | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. Outrun on `main` by ADR-0138. |
| 0052 | The invocation is the resume | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0053 | A scope narrows the set, never the rules | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0054 | The ceiling carries the isolation decision | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0055 | A collision is repaired on the losing branch, and a rebuild is the only rerun | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. Outrun on `main` by ADR-0141. |
| 0056 | A run refuses a working tree it cannot account for | DROP | — | — | Orchestrate runtime. Neither `run.py` nor `tests/test_orchestrate.py` cites it, so the `RUNTIME` ground does not reach it and the rework's bin stands even though the Skill does; the class is ADR-0139's note. |
| 0057 | A working tree belongs to the run branch it was cut from | DROP | — | — | Orchestrate runtime. Neither `run.py` nor `tests/test_orchestrate.py` cites it, so the `RUNTIME` ground does not reach it and the rework's bin stands even though the Skill does; the class is ADR-0139's note. |
| 0058 | The closed half of a scope is bounded by the branch the run is on | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0059 | An unknown subcommand and a disallowed flag are both errors | C2 | — | `skills.md` | Current law across every Skill; already stated in the standard. |
| 0060 | Frontmatter is read by a real YAML parser, and the price is the offline cold start | C3 | — | `skills.md` | Current law; the cold-start cost is the why. |
| 0061 | The collection writes one flat, prefixed `metadata` namespace | C3 | — | `skills.md` | Current law; already stated in the standard. |
| 0062 | `compatibility` states the environment, and names no product | C3 | — | `skills.md` | Current law; already stated in the standard. |
| 0063 | On-demand files live under `references/` | C3 | — | `skills.md` | Current law; already stated in the standard. |
| 0064 | A run works the branch it was left on | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0065 | The requirement is the whole thread, not the body | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0066 | The reference validator is a baseline, not a gate | C6 | — | `skills.md` | Current law with a live consequence for every new Skill; the baseline claim needs its record. |
| 0067 | A ticket asserts only what stays true until it is built | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. The rework binned it C6, and its subject is not /orchestrate's machinery; the citation criterion claims it anyway, which is what makes this one of the seven rows a reader should look at first. |
| 0068 | A declaration the Manager cannot read is not a declaration of nothing | C1 | — | `collection.md` | Current law at the dependency gate. |
| 0069 | A failed verification buys one amend, as a collision buys one rebuild | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0070 | A run asks at plan time or not at all | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0071 | What parallel tickets share, the run allocates | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0072 | The wave check reads coherence, and its fixes loop to a fixed point | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. Outrun on `main` by ADR-0171. |
| 0073 | A discovered edge corrects the graph rather than burning the ticket | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0074 | Building may be delegated down; the verdict never is | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0075 | A later record that outruns an earlier one leaves a pointer in it | C6 | — | `docs.md` | The discipline the archive needs; its cost is what the reform is removing. |
| 0076 | Shared implementation belongs to the Collection Library | C3 | — | `skills.md` | Current law; already stated in the standard. |
| 0077 | Subcommands have addressable manpages | C2 | — | `skills.md` | Current law; already stated in the standard. |
| 0078 | An Invocation Envelope separates strict grammar from contextual instruction | C2 | — | `skills.md` | Current law across every Skill; already stated in the standard. Outrun on `main` by ADR-0122. |
| 0079 | A Run Outcome is history and a Ticket Resolution is current | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. Outrun on `main` by ADR-0142. |
| 0080 | TL;DR selects for the owner of the outcome before it compresses words | KEEP | — | brief's own files | The register every new Skill adopts by reference; the perspective argument is not restatable in one line. The Skill is `brief` since ADR-0113, so the rework's `tldr` landing is renamed here. Outrun on `main` by ADR-0170. |
| 0083 | Model-selector owns exact frozen routing | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. The rework binned it C5, and its subject is not /orchestrate's machinery; the citation criterion claims it anyway, which is what makes this one of the seven rows a reader should look at first. Outrun on `main` by ADR-0136, ADR-0147, ADR-0166. |
| 0084 | A fresh amended verdict buys one continuation amend | DROP | — | — | Orchestrate runtime. Neither `run.py` nor `tests/test_orchestrate.py` cites it, so the `RUNTIME` ground does not reach it and the rework's bin stands even though the Skill does; the class is ADR-0139's note. |
| 0085 | Orchestrate routes execution and inherits verdicts | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. Outrun on `main` by ADR-0172. |
| 0087 | A Language Resource co-locates selectors and scoped guidance | C4 | — | `skills.md` | Current law for the editorial Skills. |
| 0088 | Editorial Skills compose without requiring Write provenance | C4 | — | `skills.md` | Current law. |
| 0089 | Routed work reports the evidence it never imports | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. The rework binned it C5, and its subject is not /orchestrate's machinery; the citation criterion claims it anyway, which is what makes this one of the seven rows a reader should look at first. Outrun on `main` by ADR-0137, ADR-0154. |
| 0090 | A Skill owns the Harness integrations it installs | C5 | — | `skills.md` | Current law; already stated in the standard's `kntnt.integrations` rule. Outrun on `main` by ADR-0130, ADR-0156, ADR-0158, ADR-0160, ADR-0167. |
| 0091 | Delivery is the response by default, and a source file is replaced only on request | C4 | — | `skills.md` | Current law for every Skill producing a Text Artifact. |
| 0093 | One corpus, evaluated separately inside each provider family | C4 | — | `docs.md` | Current law; `docs/evaluation/protocol.md` is where a reader meets it. |
| 0094 | A model starts a Skill only inside a description that bounds the trigger | C3 | — | `skills.md` | Current law; already stated in the standard. |
| 0095 | A first draft's requirements are stated once, and review guidance extends them | C4 | — | `skills.md` | Current law; already stated in the standard's Library section. Outrun on `main` by ADR-0164. |
| 0096 | A valued flag attaches its value with an equals sign | C2 | — | `skills.md` | Current law; already stated in the standard. |
| 0097 | One invocation order: command path, then flags, then operands | C2 | — | `skills.md` | Current law; already stated in the standard. |
| 0098 | A fully determined fix is mechanical, whatever the gate says | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. Outrun on `main` by ADR-0110. |
| 0099 | A ticket that rewrites an invariant declares that it builds alone | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. The rework binned it C6, and its subject is not /orchestrate's machinery; the citation criterion claims it anyway, which is what makes this one of the seven rows a reader should look at first. |
| 0101 | An adapted catalogue is owned rather than depended on | C4 | — | `skills.md` | Current law; the licence notice rule has a real consequence. |
| 0103 | `/brief` addresses its mode through a command path and carries no free-text operand | DROP | — | brief's own files | One Skill's grammar; the general rule is ADR-0097's. The Skill is `brief` since ADR-0113, so the rework's `tldr` landing is renamed here. Outrun on `main` by ADR-0169. |
| 0104 | A control carried by inheritance completes the point | C5 | — | `collection.md` or `routing.md` | Model-selector internals; the rule is the adapter schema's, stated in that Skill. The rework left this cell empty; the carried-control contract is what a rules module states, the adapter schema staying the Skill's. Outrun on `main` by ADR-0136, ADR-0146. |
| 0105 | The valued-flag registry derives from the collection's own declarations | C2 | — | `skills.md` | A test's construction rather than a decision; the rule is one line in the standard. |
| 0106 | A collision in generated files is regenerated, not repaired | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate runtime the rework dropped with the Skill; the Skill stays on `main`, so the record stays with it. |
| 0107 | A correction is delegated fresh and verified by review | C4 | new record | `skills.md` | The correction loop the editorial Skills share: fresh delegation, verification by review, and the budget's exits. Amended by ADR-0120. |
| 0109 | `/delegation` addresses its mode through a command path and its scope through a flag | DROP | new record | delegation's own files | One Skill's grammar, exactly as the rework read ADR-0103; the general rules are ADR-0097's and ADR-0059's and the four accepted forms are stated on the Skill's own pages. |
| 0110 | A changed-nothing fix round escalates once from a selected seat | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate's own escalated fix round, added on `main` since the fork. |
| 0112 | One lens applied alone ships narrower than the contract it belongs to | C4 | new record | `skills.md` | What a single-lens editorial Skill may reach and may not; the narrowness is the whole decision and it binds the editorial set rather than one Skill. |
| 0113 | The reframing Skill is named `brief` | KEEP | new record | — | A naming decision that stands alone: no rules module holds Skill names, the record declines to state a collection-wide rule itself, and ADR-0168's guard rests on its argument. |
| 0115 | Inferring a genre reads the installed openings and nothing further | C4 | new record | `skills.md` | Genre inference's reading licence, stated for every Skill that resolves a genre. |
| 0118 | A brief travels as its subagent's instruction and never as a file | C4 | new record | `skills.md` | How a correction brief reaches its subagent; the record says itself the rule belongs to the Collection rather than to the Skill it was observed in. |
| 0120 | A repair removes the pattern and not the claim it carries | C4 | new record | `skills.md` | The fourth exit of the correction loop; amends ADR-0107, which is in the same bin. |
| 0121 | Generic mechanics are stated once, and a clause boundary turns on whether the clauses cohere | C4 | new record | `skills.md` | The shared mechanics contract in the Library and the clause-boundary rule it states. |
| 0122 | Guidance a precedence has settled is suppressed rather than ineffective | C2 | new record | `skills.md` | Suppression is a reading of the Envelope's mixed-guidance clause, so it belongs with ADR-0078 rather than with the editorial contract it was observed in. Narrows ADR-0078. |
| 0123 | A findings report is written in the language of the text | C4 | new record | `skills.md` | The language a findings report is written in, stated once in the shared editorial contract. |
| 0124 | A named destination takes the artifact out of the response | C4 | new record | `skills.md` | Delivery to a named destination, which extends ADR-0091 in the same bin. |
| 0125 | A code sample is quoted material and produces no findings | C4 | new record | `skills.md` | What an editorial pass may not touch, stated in one wording across every editorial Skill. |
| 0127 | A wait ends with its command, and a subagent leaves nothing running | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. A Collection-wide rule about waits and leftovers, met here because /orchestrate's briefs carry it; the citation criterion claims it all the same. |
| 0129 | A scoped language result exposes content and not its backing path | C4 | new record | `skills.md` | What the Language Resource resolver exposes, which is the editorial family's own Interface. |
| 0130 | A refresh publishes only a verified complete generation | C1 | new record | `collection.md` | The refresh transaction: staging, verification, atomic publication. Narrows ADR-0001, ADR-0028, ADR-0036, ADR-0041 and ADR-0090, all of which stay in their own bins. |
| 0131 | A Global Update is authorized by the current exact plan | C1 | new record | `collection.md` | What authorizes a Global Update, which is the Manager's own two-phase gate. |
| 0132 | Model Selector is model-invoked at dependent Interfaces | C5 | new record | `collection.md` or `routing.md` | When model-selector is model-invoked, which is the routing chain's entry. Narrowed by ADR-0133, ADR-0136, ADR-0137 and ADR-0154, each in this bin. |
| 0133 | A spawn on the frozen main seat is unrouted by the caller's choice | C5 | new record | `collection.md` or `routing.md` | The unrouted main-seat spawn. Narrowed by ADR-0156 and ADR-0172; ADR-0172 is RUNTIME and the pointer stays where it is. |
| 0134 | Execution takes one of three paths, chosen by the shape of the work | C5 | new record | `collection.md` or `routing.md` | Which of three paths an execution takes. Binned with routing rather than dropped to the Skill's own files because the choice is the delegation half of the routing chain and ADR-0151 reasons from it. |
| 0135 | A delegation report is written in scratch and capped inline | C5 | new record | `collection.md` or `routing.md` | What a delegation brief asks back and where it is written. The same judgement as ADR-0134 and the weakest of the C5 rows: no file outside `docs/adr/` cites it. |
| 0136 | Model Selector derives routing context from shipped adapters | C5 | new record | `collection.md` or `routing.md` | The Context Interface and the adapters it derives from. Narrowed by ADR-0165 and ADR-0166. |
| 0137 | Orchestrate imports machine-judged observations at verdict | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate's own import of machine-judged observations, added on `main` since the fork. |
| 0138 | Declared commit roles are checked before integration | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate's own role check, added on `main` since the fork. |
| 0139 | A wave verdict proves a load flake before passing | DROP | new record | /orchestrate's own files | Orchestrate machinery neither `run.py` nor `tests/test_orchestrate.py` cites, so the RUNTIME ground the ticket states does not reach it and the rework's bin for orchestrate records stands. The first class to correct by hand if uncited machinery is meant to survive. |
| 0141 | A parked ticket resumes its lifetime attempt | DROP | new record | /orchestrate's own files | Orchestrate machinery no engine or suite file cites; same reading as ADR-0139. Narrows ADR-0055, which is RUNTIME. |
| 0142 | Reconciliation can resolve a parked ticket | DROP | new record | /orchestrate's own files | Orchestrate machinery no engine or suite file cites; same reading as ADR-0139. |
| 0143 | A run may be bound to its first plan | DROP | new record | /orchestrate's own files | Orchestrate machinery no engine or suite file cites; same reading as ADR-0139. |
| 0144 | The first approved payload is an authorization ceiling | DROP | new record | /orchestrate's own files | Orchestrate machinery no engine or suite file cites; same reading as ADR-0139. |
| 0145 | A ledger row becomes evidence only inside its own Cohort | C5 | new record | `collection.md` or `routing.md` | What makes a ledger row evidence. Narrowed by ADR-0156. |
| 0146 | A Rung is the next model where deliberation is exhausted or carried | C5 | new record | `collection.md` or `routing.md` | What a Rung is, in both dimensions. Supersedes ADR-0104 in the escalation dimension alone. |
| 0147 | The frozen objective orders a frontier nothing else can | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Model-selector's frontier ordering, met here because the engine reasons from it; the citation criterion claims it. |
| 0148 | The merge that brings a resumed ticket forward is run-owned history | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Orchestrate's own resume history, added on `main` since the fork. |
| 0149 | A Cohort starts where its Standing Policy says, and only a reset lowers it | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Model-selector's Standing Policy start, met here because the engine reasons from it; the citation criterion claims it. |
| 0150 | Verified failures ratchet a Cohort at the import that recorded them | C5 | new record | `collection.md` or `routing.md` | The ratchet that moves a Cohort's Standing Policy. Narrowed by ADR-0159. |
| 0151 | An Exploration Attempt buys contrast one Rung down, on a budget | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Model-selector's Exploration Attempt, met here because the engine reasons from it; the citation criterion claims it. |
| 0152 | An engine that reads its own command line parses one grammar the Library owns | C2 | new record | `skills.md` | The flag-presence rule and the Library's ownership of the grammar the two self-parsing engines read; #269 names the flag-presence rule as part of this bin. |
| 0153 | The experiment brief and the routing decision read one ladder | C5 | new record | `collection.md` or `routing.md` | The experiment brief reading the routing decision's own ladder. |
| 0154 | Delegation files machine-judged evidence in one Cohort | C5 | new record | `collection.md` or `routing.md` | What delegation may file without asking, and where. |
| 0155 | The review brief names the builder and logs what the reviewer supplied | C6 | new record | `tickets.md` | Who a ticket is written for and what the readiness review logs, which is the ticket layer's own law. |
| 0156 | Ordinary work is measured, never judged | C5 | new record | `collection.md` or `routing.md` | Usage Records beside the evidence ledger. Narrows ADR-0090, ADR-0133 and ADR-0145. |
| 0157 | An adapter is verified against its own Harness, and a trust gate is reported gated | C5 | new record | `collection.md` or `routing.md` | How an owned integration is verified and how a trust gate is reported, which is ADR-0090's ground. |
| 0158 | The finished session's own record is read once, at the hook that ends it | C5 | new record | `collection.md` or `routing.md` | What the session-ending hook may read. Narrows ADR-0090. |
| 0159 | Evidence reset takes a ratcheted Cohort's Standing Policy down with it | C5 | new record | `collection.md` or `routing.md` | What an evidence reset takes with it. Narrows ADR-0149 and ADR-0150. |
| 0160 | Capture follows the Skill's own Enabled state | C5 | new record | `collection.md` or `routing.md` | Capture following the Skill's Enabled state. Narrows ADR-0090. |
| 0161 | Observed usage joins a recommendation by model and portable deliberation | C5 | new record | `collection.md` or `routing.md` | How observed usage reaches a recommendation. Narrowed by ADR-0162 in the join key alone. |
| 0162 | Observed usage joins on the model alone | C5 | new record | `collection.md` or `routing.md` | The join key. Narrows ADR-0161. |
| 0163 | The genre orders the document and the technique orders its sections | C4 | new record | `skills.md` | What a genre orders and what a technique orders, which is the editorial contract's own division. |
| 0164 | A genre names the technique it is ordinarily written with | C4 | new record | `skills.md` | A genre naming its ordinary technique. Amends ADR-0095, which is in this bin. |
| 0165 | A stored profile that does not validate is rejected, not absent | C5 | new record | `collection.md` or `routing.md` | Rejected against absent in the stored profile. Narrows ADR-0136. |
| 0166 | An unranked main seat suspends the ceiling it cannot state | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py`. Model-selector's unranked main seat, met here because the engine reasons from it; the citation criterion claims it. |
| 0167 | An unattended pass may learn what a model can do, never what it costs | C5 | new record | `collection.md` or `routing.md` | What an unattended maintenance pass may learn. Narrows ADR-0090. |
| 0168 | A retired name is free for the Skill it fits, and the guard keeps one Skill's surfaces | C3 | new record | `skills.md` | A rename guard reads one Skill's own surfaces rather than the tree's strings, and a name a Skill was renamed away from is available to a Skill it fits: a rule about Skill form and naming, which is `skills.md`'s ground. Narrows ADR-0113, which is `KEEP`. |
| 0169 | The reserved separator is optional where a Skill's grammar has no command path | C2 | new record | `skills.md` | When the reserved separator is optional, which is ADR-0078's own grammar. Narrows ADR-0103. |
| 0170 | Brief mode belongs to the conversation it is typed in and persists nothing | C2 | new record | `skills.md` | Brief mode's scope and its invalid bare form. The why-chain worth carrying is the Output Style declined a second time, which is the one thing the Skill's own files cannot hold and which the record exists to keep from being proposed a third time. |
| 0171 | The wave check reads the wave it merged, and not the whole branch | RUNTIME | new bin | — | Cited by `tests/test_orchestrate.py`. Orchestrate's own wave check, added on `main` since the fork. |
| 0172 | A frozen account that inherits for the run restates its own decision for later roles | RUNTIME | new bin | — | Cited by `skills/code/orchestrate/scripts/run.py` and `tests/test_orchestrate.py`. Orchestrate's own restated inheritance, added on `main` since the fork. |

## Counts

| Bin | Records |
|---|---|
| `C1` — the distribution model | 25 |
| `C2` — the invocation grammar | 11 |
| `C3` — what a Skill ships | 13 |
| `C4` — the editorial contract | 18 |
| `C5` — routing and evidence | 21 |
| `C6` — decisions and tickets | 3 |
| `DROP` — rules already in a Skill's own files, or already superseded | 15 |
| `DROP` — orchestrate machinery nothing outside `docs/adr/` cites | 9 |
| `KEEP` | 2 |
| `RUNTIME` | 36 |
| **Total** | **153 → 44 after the reform: 2 kept, 36 runtime, and the 6 consolidation records** |

## Where else instructions live

The rework's inventory, brought up to date against `main`.

| Place | What it holds | Bearing on the reform |
|---|---|---|
| `docs/coding-standard/general.md` | Code form, design philosophy, refactoring completeness, naming, packaging, tooling | Already the rules-doc format. Absorbs, does not compete. Becomes `docs/rules/general.md` in #263. |
| `docs/coding-standard/python.md` | Python baseline, PEP 723, tooling | Unaffected beyond the rename. |
| `docs/coding-standard/skills.md` | What a Skill ships: frontmatter, body, grammar, Library, manpages, Codex sidecar, README | Already the rules doc for Skill form; 53 record citations point out of it. #261 rewrites its grammar section before the reform reaches it. |
| `CONTEXT.md` | Domain glossary — in practice, the Manager's behavioural spec, and 4 record citations | Needs a decision: glossary or law. #265 holds it to definitions once `collection.md` exists. |
| `AGENTS.md` | Ground rules and the `read when` References lines, two of which point at individual records by path — ADR-0067 and ADR-0099 | The router. Gains a line per rules module; the two record lines collapse into #266's one. |
| `CONTRIBUTING.md` | The four checks, catalog regeneration, the reference-validator comparison; cites ADR-0066 and ADR-0106 | Procedure. Both records it cites survive the reform — ADR-0066 into the C6 record, ADR-0106 as `RUNTIME`. |
| `agents.d/user-configuration.md` | User-owned configuration for a Skill: where it lives and who may write it | Added since the fork. Unaffected. |
| `docs/evaluation/protocol.md`, `docs/evaluation/corpus/`, `docs/evaluation/records/` | The evaluation protocol, its fixture corpus, and the records of runs against it | Unaffected; ADR-0093's rule lands in `docs.md` beside it. |
| `docs/research/` | The manpage and anti-slop research notes, the invocation-mechanics problem statement, and this table | Cites records, and is now inside the suite's citation scan. This file is deleted by #272; the others stay. |
| `docs/archive/claude-skills/` | Two inactive Skills from the former repository, historical only | Outside the collection. Unaffected. |
| `skills/kntnt/library/references/` | The invocation Envelope, delivery, the changelog format, and the editorial and language resource sets with their own format pages | Unaffected; already the right shape. #261 gives the Envelope contract its file here. |
| Each Skill's own `SKILL.md`, `help.md`, `references/` | That Skill's behaviour, and 230 record citations | Where a one-Skill rule belongs. Already carries most of them; #272 repoints what it cites. |
| `tests/test_adr.py` | Numbering uniqueness, citation resolution, outrun pointers in both directions, hand-listed relation pairs, and this table's completeness | Rewritten by #272: numbering and citation resolution stay, the relation machinery and the triage checks go with the duty and the file they hold. |
| `tests/` as a whole | 1 000 record citations in assertion messages | Every citation of a deleted number is repointed by #272. |
