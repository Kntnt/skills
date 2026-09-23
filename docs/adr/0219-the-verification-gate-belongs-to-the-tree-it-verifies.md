# The verification gate belongs to the tree it verifies

Orchestrate hands every subagent that verifies work a list of commands, the gate, read from the project's contributing guide. Since issue #80 the orchestrator read that guide once at run start and held the list for the whole run. This record replaces that rule: the gate filled into a brief is the gate the guide states in the tree where that brief's subagent works or verifies. What the rule now is is stated in the Skill's own shipped files, `skills/code/orchestrate/SKILL.md`, its briefs and `help.md`. This record argues the case (issue #421).

## What the run of 2026-09-23 showed

**The guide is a file tickets edit.** The run that built #405–#410 at a concurrency of four changed the mypy line in `CONTRIBUTING.md` five times: #406 added `credentials.py` in the first wave, and each ticket of the second wave added its own engine. After #408 merged mid-wave, the orchestrator read the guide again from the run branch and gave #410's verifier a line naming `nodeping.py`, which #408 had added and #410's tree, forked at the wave start, did not have. mypy refused the missing file and the verifier failed a ticket whose every criterion was met. The orchestrator then pinned the gate at the wave-start commit and the same verdict passed.

**Every way of holding the gate for the run or the wave was wrong.** Held from run start, as the Skill said, no verdict of the run type-checked any of the five engines the run added. Pinned at the wave start, no second-wave verifier type-checked the one module its own ticket added, and the repair verifiers ran that gate on merged trees holding engines it did not name. Read from the run branch as it moves, the gate named files a tree forked earlier did not have. The same seam appeared from the other side on 2026-09-07, when #293 removed a module from the line and the gate held from run start went on naming it.

## The decision

**The gate is a property of the tree.** A ticket's verifier and both attempts of an amend read the ticket's working tree as it stands when the brief is filled. The repaired-collision verifier reads the repaired tree after the merge. The repair builder, whose brief is filled before it merges, reads the run branch as it stands and is told its verdict runs the merged tree's gate. The wave check and every rerun of it read the run branch as it stands when that round is briefed, and so does the branch gate a concurrency-of-one run takes before it reports. The builder is handed the gate of its own working tree too, which it was not before.

**The engine picks the tree and keeps the readings; the reading stays the orchestrator's.** `run.py gate --ticket=<number>` resolves the ticket's working tree from what `isolate` made, or the run branch where the ticket is built on it, and answers the guide's blob in that tree and in its base with the reading recorded under each. The orchestrator reads the guide only for a blob that has no reading and records its list through the same verb, into the state directory. A guide that is byte-identical to one already read is not read again, so a wave in which no ticket touches the guide reads it once, as before. A tree with no guide keys its reading on the commit it stands at. The readings are remembered rather than relied on: the guide at every recorded blob stays in Git.

**What issue #80 fixed stays fixed.** No subagent reads the guide to derive its own gate, and no brief lets its subagent widen the list. Neither fix needed the list to be frozen for the run.

## The trade-off, and what answers it

**A ticket can now change the gate it is held to.** That is the point of the change, and it is also its risk: a ticket that drops or narrows a command it was not asked to change would be verified against the weaker list it wrote. So the ticket and repaired verdicts are shown the gate of the tree's base beside the tree's own, for comparison and never to run, and each checks for a command the base names that the tree dropped or narrowed, the same way it already checks for a test weakened or deleted to make something pass. The base is computed by the engine: the merge-base of the ticket's branch and the run branch for a ticket with a working tree, the run head a repair merged in for a repaired tree, and the start point of the serial build episode at a concurrency of one. The builder is told the same rule, so that the comparison is a check and not a surprise.

## The alternatives

**The orchestrator reads again per tree, keyed on the guide's content, with no engine verb.** It is cheap, and it keeps the reading where it belongs. It leaves the orchestrator choosing the tree by hand, and a tree chosen by hand is what went wrong on 2026-09-23. Once the base had to be computed as well, this was no longer a prose-only change anyway.

**Read the gate again at each wave start, from the run branch.** It is what the run fell back to and the smallest change. It is wrong both ways the run showed: it misses the module a ticket adds in its own wave, and it runs a gate on repaired trees that does not name what they hold.

**A machine-readable declaration of the gate in the repository**, beside `.kntnt-orchestrate/generated.json`. With it the engine could extract the commands without any reading. It would be a third copy of this repository's mypy line, beside `CONTRIBUTING.md` and `.github/workflows/ci.yml`, and every repository would have to adopt the new file before the fix reached it.

## What this leaves out

**A single shared type-check line still makes tickets collide.** Three of the second wave's four tickets went through collision repair over that one line in `CONTRIBUTING.md`. Moving the list out of one shared line, into a mypy configuration file for example, is a change to this repository and not to the Skill, and it is not made here.
