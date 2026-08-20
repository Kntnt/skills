# A declaration the Manager cannot read is not a declaration of nothing

Every Skill of this collection runs a dependency gate before it does anything, and that gate could answer exit 0 with two empty lists for a Skill declaring a binary that does not exist and a Capability the Harness may not have. It failed open on both halves without a word. `skill_deps` reads the four Dependency lists out of the `metadata` keys prefixed `kntnt.` that ADR-0061 flattened them into, and a frontmatter carrying no such key came back as four empty lists — which is exactly what a Skill that genuinely requires nothing comes back as. A Manager reading a shape it does not know is therefore indistinguishable, to everything downstream, from a Manager reading a Skill with nothing to declare. **A Skill that asks this Manager what it declares, and whose declaration this Manager cannot read, is refused rather than read as requiring nothing** (issue #68).

That is worse than a refusal that should not have happened. Each Skill's body says *Exit 2: emit stdout and stop*, so exit 0 is the go-ahead and the Skill runs; the Capability half is worded *Exit 0 is not a go-ahead until every one is answered*, and an empty list has nothing to answer, so the agent proceeds having answered nothing. A gate that refuses when it should not is found the first time somebody runs it. A gate that admits when it should not is never found at all.

## The state is reachable, and by which verbs

The question this record was written to answer first: can any Manager verb place a Skill carrying the current `metadata` shape into a layer whose Manager still carries the previous one? **It can.** The parser in `parse_args` is the collection's one table of verbs, and it carries eight: `help`, `manpage`, `check`, and `catalog`, plus `select`, `update`, and `uninstall` under each of `plan` and `apply`. That list is exhaustive by construction — there is no second grammar for it to disagree with — and only the three `apply` verbs write Skills into a layer. Each was run against the transport with its calls logged:

| Verb | Names the Manager to the transport | Reaches the state |
|---|---|---|
| `apply select`, Global | no | **yes** |
| `apply select --project` | no | **yes** |
| `apply update`, Global | yes, and first | no |
| `apply update --project` | no | **yes** |
| `apply uninstall` | removes only | no |
| `plan select`, `plan update`, `plan uninstall` | write nothing outside a Sandbox | no |
| `help`, `manpage`, `check` | write nothing | no |
| `catalog --write` | writes `catalog.json` beside the Manager | no |

The Manager is no Catalog entry, so `select_change` — which iterates the Catalog — never names it, in either layer. `refresh_change` prepends it, which is why `apply update` on the Global layer refreshes the Manager and every Enabled Skill in one call and leaves the machine consistent. It prepends it only there: an Update of a Project places no Manager in the working directory, and a Project Skill's checker falls back to the Global Manager, so `apply update --project` refreshes Skills against a Manager it did not touch.

So `/kntnt update` is the migration path and it does close the gap, but it is not the only path a user can take. `select` is a verb a user reaches for to Enable one Skill, it fetches from the origin like every other verb, and it refreshes no Manager — which makes *Enable a Skill on a machine that has not run Update since the shape changed* an ordinary thing to do rather than a mistake. The hazard is not closed by release ordering.

## The two questions that looked like one

`collection_block` answering `None` is how the Manager tells a stranger's Skill from one of its own, and a stranger's Skill legitimately has no Dependencies for this Manager to check. A rule of the form *refuse where the block is missing* would refuse every Skill on the machine this collection did not write. That is why the fail-open shape survived: refusing looked like it cost more than it bought.

**The two states come apart at the caller.** `carries_marker` asks a directory the collection did not write whether it is ours, and may not raise about any of them; the gate asks a Skill that invoked the checker itself what it declares. Nothing but a Skill of this collection invokes the checker — the instruction to run it is written in the collection's own Skill bodies, and it is the first thing each of them does. A caller is one of ours by the act of calling, so at the gate no readable declaration means *ours, and unreadable*, while at the sweep it goes on meaning *not ours*. One predicate, `marker_fault`, answers both; the two callers read its answer differently because they asked different questions. Nothing about the marker's shape changes, and neither does `carries_marker`, which still answers rather than raising, whatever it meets.

**The refusal is exit 2 with the reason on stdout, not a raised error.** Exit 2 is the one non-zero answer every Skill's body documents a response to, so a fault reported that way reaches the user through a channel that already exists; a raised error exits 1 to stderr, and a Skill told only what to do with exit 2 would stop with nothing to say. The entry carries the same three keys every Unsatisfied Dependency carries, because the instruction is *emit stdout*, and an entry of another shape reaches the user through no documented channel at all. What is Unsatisfied is the declaration itself, so the entry names the Skill, gives `declaration` as its kind, and gives the fault and the remedy — refresh the machine with `/kntnt update`, which is what brings the Manager and every Enabled Skill to one revision.

**Update reports it rather than refusing.** The same predicate now guards `apply update`'s re-check of every Skill the layer holds, and there it may not raise: the withdrawals are already deleted and the placements already made by the time the loop runs, and a change the disk shows and nothing says is what ADR-0036 forbids. Update reaches Skills a refresh could not repair — one the origin was unreachable for, one a hand edit left with no frontmatter at all — and each of those is precisely what has to appear in the report.

## What this does not do

It does not read both shapes. The collection migrates rather than accepting both, which is settled and is why the flat namespace landed as it did (ADR-0061), and nothing here is an accommodation of the shape it replaced. It does not change that namespace, which is what the specification asks for. It does not touch the Capability mechanism, which behaves exactly as designed once it is given a list to work with.

**It cannot reach a Manager already on a machine.** The code that fails open is the installed Manager's, and this change is in the collection's. For the migration that produced the finding, the residual hazard stands as described above: a machine that Enables a Skill by `select` without first running `update` gets the new shape beside the old Manager, and that old Manager will answer exit 0 with two empty lists. What this record buys is the next one. A shape change after this one is caught at the gate on the machine where it happens, rather than being invisible in exactly the way this one was.

The generation-time gate is unchanged and still needed. `catalog` refuses every unreadable marker in the repository, and `CONTRIBUTING.md` step 4 regenerates the Catalog before anything ships, which is what keeps a malformed Skill from leaving here. That pair was described as the whole of the guarantee; it was the whole of the guarantee about the repository, and never about a machine holding two revisions at once.
