# redline — claude — 2026-08-26

- **record** — `redline-claude-2026-08-26`
- **date** — `2026-08-26`
- **ticket** — `#160`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.246
- **corpus commit** — `46ba9c1`

## Run conditions

The Skill was run against the copy installed at `~/.claude/skills/redline`. `diff -r` reported that directory byte-identical to `skills/editorial/redline/` at the corpus commit, and the same for `~/.claude/skills/proofread` against `skills/editorial/proofread/` — the one peer Skill Redline declares, which its step 9 follows — and for `~/.claude/skills/kntnt/` against `skills/kntnt/`, the Manager and the Collection Library both of them resolve through. The only difference anywhere was the untracked `__pycache__` directories the repository working tree carries and an installed copy does not.

Each fixture ran in a Claude Code agent session of its own, started from this session, with no memory of any other run and no access to this repository's evaluation material: the turn carried the invocation and nothing else, and no run was given the ticket or the criteria below. Each ran in its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says — `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form.

**side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself.

**What the inventory covered, and what it did not.** The inventory above is taken over the staged copy of the corpus and nothing else, so a file written outside it would not have appeared in any entry's **side effects**. The Write evaluation for the same date found that this matters — one of its runs wrote its artifact into the Harness's scratchpad while reporting that nothing had been written, which is #180. The same check was made here: at the end of the session the scratchpad held nothing this Skill's runs had put there.

**How the Skill was started.** Redline carries `disable-model-invocation: true`, so the Skill tool refuses to start it from inside a turn and a sub-session never receives an expanded slash command. Each run was therefore handed what the Harness itself gives a user-invoked Skill: the installed `SKILL.md` named as the turn's instructions, with `$HERE` named as the directory holding it. The run read that file from disk and followed it — the checker it runs, the resolver it runs, every reference it loads, the correction subagents it starts, and the peer Skill its step 9 follows. A user-invoked Skill's body is static instructions rather than a preprocessed template, which is what makes this the same seam rather than an imitation of one; the Write record for the same date sets the reasoning out in full, and the sixteen refusals that established the constraint are recorded there.

Judging was done from the delivered reply and the filesystem inventory alone, against the criteria below, fixture by fixture, before any GPT-family record existed to compare with. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

The criterion identifiers are stable across entries: `review` (the initial review finds what is there, located and named), `budget` (the Correction Budget is a ceiling spent as the contract says), `fresh` (each correction goes to a subagent started fresh, carrying the complete current text and the complete current findings), `verify` (a correction is verified by a fresh review rather than accepted on its own report), `stop` (the loop stops at one of the four conditions and says which), `no-source` (no source-verification commentary anywhere), `mechanics` (the mechanical pass runs exactly once, after all review and correction, and nothing substantive follows it), `unresolved` (findings left over are delivered with the artifact and named as unresolved, routed as the destination requires), `handoff` (a recognized map is synchronized to the resolved configuration and nothing else in the frontmatter moves), `preserve` (material outside the findings comes through untouched), `code` (a code sample produces no finding and comes back byte for byte), `resolution` (each parameter settled at the level the precedence gives it), `ask` (a materially mixed language is asked about rather than guessed), `leak` (the reasoning, the dismissed passages, and any correspondence with a subagent or the nested Skill stay out of the output), `target` (the artifact went where the output contract sends it), `effects` (the filesystem shows what the contract allows and nothing else), and `refusal` (a refused invocation names the problem, prints the synopsis, points at help, and leaves nothing behind).

## `slop-heavy` (review only, budget zero)

- **fixture** — `slop-heavy`
- **invocation** — `/redline --max=0 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text, unchanged, followed by eleven numbered findings, each located and named, and a line saying the budget was `0` so every one of them is unresolved.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — eleven findings on a text built out of the catalogue, and each is named rather than disliked: the empty opening, the four false contrasts quoted in full, the three unattributed authorities, importance inflation listed item by item, the three consecutive anaphoric paragraphs, the synonym cycling, the restatement of paragraph 2 in paragraph 4, three connectives claiming relations that do not hold, and the closing that restates the opening as a rhetorical question.
  - `budget` — `pass` — `0` spent nothing, and no correction subagent was started.
  - `mechanics` — `pass` — the mechanical pass still ran and reported finding nothing, which is what `--max=0` is specified to leave in place.
  - `no-source` — `pass` — nothing anywhere asks for the studies, the experts, or any material behind the text; the unattributed authorities are found as an editorial defect visible inside the artifact, which is the right way for this Skill to reach them.
  - `unresolved` — `pass` — all eleven are delivered with the artifact and named as unresolved.
  - `preserve` — `pass` — the text came back as it arrived.
  - `leak` — `pass` — no reasoning, no dismissed passages, no correspondence.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — eleven.
- **defects filed** — none.
- **notes** — finding 1 says explicitly that it cannot be repaired by editing because the specifics would have to be invented. That is the review declining to hand a correction round an impossible instruction, and it is the right shape for a finding a budget cannot spend itself on.

## `slop-heavy` (default budget)

- **fixture** — `slop-heavy`
- **invocation** — `/redline $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text, much shorter, then four unresolved findings and a list of what the round repaired.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — thirteen findings on the first pass, four standing after the re-review.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the returned text was reviewed again and the findings from that re-review, not the subagent's account, are what the reply carries.
  - `stop` — `pass` — the loop stopped on the third condition and says so: finding 3 is a defect the text did not arrive with and the round's own cut created, and the reply names it as the reason another round would have been repairing its own work.
  - `unresolved` — `pass` — four carried forward, each with what it would take to settle it.
  - `no-source` — `pass` — the unattributed authorities were cut as unsourceable rather than sent back for sources, and nothing remarks that material was unavailable.
  - `mechanics` — `pass` — once, after the correction, reporting no error.
  - `preserve` — `pass` — what survives is what the findings did not name; the reply lists what was removed and every item on it is a finding.
  - `leak` — `pass`.
  - `target` — `pass` — response, and the source file on disk is byte-identical to the corpus.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — four, one of them created by the run's own repair and named as such.
- **defects filed** — none.
- **notes** — the corrected text is two short paragraphs from a six-paragraph draft. That is what the corpus's own rejection anticipates — *a correction that removes the patterns and the content with them* — and it is not what happened: the reply's finding 1 says the text now claims no more than it can hold and simply holds very little, because what was cut was the unsupportable and not the supported. There was nothing else in the draft to keep.

## `slop-heavy` (budget of three)

- **fixture** — `slop-heavy`
- **invocation** — `/redline --max=3 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text, then seven unresolved findings, then a closing paragraph headed *Why two corrections went unspent*.
- **side effects** — none.
- **criteria** —
  - `budget` — `pass` — three available, one spent, two unspent, and the reply says why rather than leaving the arithmetic to the reader.
  - `stop` — `pass` — the same third condition, and this is the entry that shows it is a stop rather than an exhaustion: findings 3 and 4 are both marked **New, and created by the correction itself**, and the run names each as the orphan or collision a particular cut left behind.
  - `review` — `pass` — seven findings after the re-review, each located.
  - `verify` — `pass` — the re-review is what produced them.
  - `unresolved` — `pass` — all seven carried forward.
  - `no-source` — `pass` — finding 2 says the unattributed claims were cut rather than sourced, *as they must be*, and that nothing may be invented to fill the gap.
  - `mechanics` — `pass` — once, after the correction.
  - `leak` — `pass`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — seven.
- **defects filed** — none.
- **notes** — this run inferred `article` where the two above inferred `general`, from the same text and with nothing naming a genre. Both sit at the fifth level of the precedence, both were named in the reply, and the findings differ accordingly rather than arbitrarily — the `article` run's findings 1 and 7 are about an angle and an arrangement that the `general` contract does not ask for. It is what an inferred genre looks like, and it is recorded rather than judged.

## `slop-heavy-sv` (review only, budget zero)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/redline --max=0 $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text with five mechanical corrections applied, then fourteen findings in Swedish, ordered by what they cost the reader, all of them unresolved.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — Swedish inferred, and the whole report about the text is in Swedish, which the delivery contract requires of a report about an artifact rather than about an invocation.
  - `review` — `pass` — this is the criterion the fixture exists for, and it is the strongest single result in the record. The catalogue is written in English and applied by what each pattern does: the run found the Swedish empty openings and closings by name (*I dagens snabbrörliga värld*, *Sammanfattningsvis*, *I slutändan handlar det om*, *Framtiden får utvisa*), the imported false contrast, the metaphor stock as a set (*en resa*, *navigera i landskapet*, *hörnstenen i*, *ta det till nästa nivå*, *nyckeln till framgång*), superlative inflation, five wholesale-translated hedges in one paragraph, the triad reflex with both triads quoted, synonym cycling across four names for one thing, the mechanical rhythm of two paragraphs, and three empty attributions in one paragraph. Not one finding is phrased as a style preference.
  - `budget` — `pass` — `0`, nothing spent, no subagent started.
  - `mechanics` — `pass` — the closing pass ran and corrected five items, which is what `--max=0` leaves in place.
  - `unresolved` — `pass` — fourteen, delivered with the artifact.
  - `no-source` — `pass` — the three unattributed authorities are found as a defect in the artifact, not as a request for sources.
  - `preserve` — `pass` — every pattern is still in the delivered text, since nothing substantive was corrected.
  - `leak` — `pass`.
  - `effects` — `pass` — the inventory is identical before and after, and the reply reports having removed its own temporary working file.
- **unresolved findings** — fourteen.
- **defects filed** — #167.
- **notes** — the mechanical pass here corrected the em dash, the comma after `Dessutom`, the curly quotation marks, and the serial comma. Three of those four are named only in the `sv` resource's **Anti-slop** section, which the mechanical pass may not load — the same divergence #167 was filed on from the Proofread runs. The run's own finding 14 names `&` for *och* as a wording choice the mechanical pass left alone, which is the boundary drawn in the other direction and drawn correctly.

## `flawed-en-US` (default budget, response)

- **fixture** — `flawed-en-US`
- **invocation** — `/redline $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line naming two substantive findings repaired in one round, the list of mechanical corrections, and the complete corrected text.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — two findings, both located: a stock opener the paragraph does not need, and a dangling clause implying a consequence the text does not support.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-review is what established that nothing remained.
  - `stop` — `pass` — stopped clean after one round.
  - `mechanics` — `pass` — after the correction, once; the American `normalize` and `catalog` survived it, and the negative-positive comma joint was kept with the mechanics contract named as the reason.
  - `no-source` — `pass` — nothing asks for the importer, the tickets, or anything behind the text.
  - `preserve` — `fail` — **an incorrect side effect on the text**, judged against the correction brief this Skill hands its own subagent. The clause *the finance team got a new reporting tool the same month* was deleted with the defect. The brief is explicit that where a passage carries a claim beside the defect, the smallest change is the one that leaves the claim standing, and that deleting the passage entire is not that change — and a smaller change was available and obvious: splitting the sentence at the joint, which is exactly what the shared mechanics contract prescribes for that comma and what every Proofread run over this fixture did. The fact went instead.
  - `leak` — `pass`.
  - `target` — `pass` — response, and the source is byte-identical to the corpus.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #179.
- **notes** — the other deletion, *The decision to rewrite it wasn't taken lightly*, is the one the previous Claude record for this Skill recorded rather than resolved: the corpus's floor for this fixture is written for a mechanics-only pass, and Redline's contract puts substantive correction in its own scope, so a hedge by the corpus's reading is throat-clearing by the review's. That judgement is unchanged here. The reporting-tool clause is a different case and a new one, because it is not a hedge — it is a fact, and the brief has a rule about facts that a smaller repair would have honoured.

## `flawed-sv`

- **fixture** — `flawed-sv`
- **invocation** — `/redline $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish line saying no substantive findings remain and only mechanical errors were corrected, then the complete corrected text.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — the review raised no substantive findings, and the reply says what it checked and found sound: the text opens on its material, holds one movement per paragraph, keeps its connectives honest, stays concrete, and ends on a point rather than a summary. A review that finds nothing in competent prose is the counterpart to one that finds fourteen things in slop.
  - `language` — `pass` — Swedish inferred; the report about the text is in Swedish.
  - `budget` — `pass` — the default `1`, unspent, because there was nothing to correct.
  - `stop` — `pass` — the first condition: no findings, budget left over.
  - `mechanics` — `pass` — once, correcting the six planted errors, and `hen` left standing.
  - `preserve` — `pass` — the argument, the numbers, and the paragraph order are as they were.
  - `no-source` — `pass`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the delivered text is not a no-change status, because the mechanical pass did change something; the contract's no-change status is for a run that changed nothing at all, which is `clean-en-GB` below.

## `clean-en-GB`

- **fixture** — `clean-en-GB`
- **invocation** — `/redline $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence: reviewed as `general` in `en_GB` with no technique, and nothing needed changing.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — nothing found in prose the corpus built to be competent, and nothing proposed.
  - `budget` — `pass` — the default `1`, unspent.
  - `stop` — `pass` — the first condition.
  - `mechanics` — `pass` — once, finding nothing.
  - `preserve` — `pass` — `judgement`, `summarise`, `towards`, `fortnight`, and the absent serial comma all stand.
  - `unresolved` — `pass` — none to carry.
  - `effects` — `pass` — the inventory is identical before and after; a response-targeted run that changed nothing wrote nothing and returned the short status.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the entry that shows the no-change status is reachable through a Skill that has a review, a budget, and a nested mechanical pass in front of it.

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/redline $RUN/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence: reviewed against the general genre in British English with no technique applied, and nothing needed changing.
- **side effects** — none.
- **criteria** —
  - `technique` — `pass` — this is the fixture's whole question. No technique was inferred despite the text's shape, none was reported, and none was acted on; the run says so in as many words.
  - `review` — `pass` — the run states its reasoning for finding nothing: the *But* and the *Therefore* each mark a relation that genuinely holds, and *The machine did not fall over* corrects a belief a reader would actually hold rather than knocking down a position nobody took. Those are the two things an anti-slop pass would most plausibly have misread here.
  - `budget` — `pass` — unspent, nothing to correct.
  - `stop` — `pass` — the first condition.
  - `mechanics` — `pass` — once, finding nothing.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — a false-contrast finding on the *But* would have been the failure this fixture is built to catch, and the run reached the opposite conclusion with the reason stated.

## `mixed-language`

- **fixture** — `mixed-language`
- **invocation** — `/redline $RUN/corpus/prose/mixed-language.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one question and nothing else, headed *language not settled*, quoting two code-switching sentences, naming the three installed candidates, and saying that nothing was reviewed and nothing was written.
- **side effects** — none.
- **criteria** —
  - `ask` — `pass` — the language was asked about before the review rather than guessed, which is what step 4 requires.
  - `resolution` — `pass` — the reply walks the precedence out loud: no `--language`, no frontmatter and so no map, nothing in the turn, leaving inference, which the text does not support.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none; nothing was reviewed.
- **defects filed** — none.
- **notes** — the reply also offers the shape of a Contextual Instruction that would say the code-switching is deliberate. That is an offer rather than an action, and it is the useful half of asking.

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/redline --output=$RUN/out/archive.md $RUN/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/archive.md`
- **observed delivery** — the reply named the three values and where they came from, named the destination, and listed two resolved findings and one unresolved one; the text was not repeated.
- **side effects** — `out/archive.md` created. The source is byte-identical to the corpus, frontmatter included.
- **criteria** —
  - `resolution` — `pass` — genre, technique, and language all from the map, which is the second level of the precedence and the level this fixture stages.
  - `handoff` — `pass` — the delivered file carries `article`, `abt`, `en_GB`, which is what the run resolved; the map already said so, so synchronizing it changed nothing, and nothing else in the frontmatter moved.
  - `review` — `pass` — two findings, both located: a title naming the subject rather than the claim, and a false contrast opening the closing paragraph.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-review is what raised finding 3.
  - `stop` — `pass` — the third condition, and the reply names the repair the new finding followed from: the title rewritten to the angle took a position on the question the article deliberately leaves open.
  - `unresolved` — `pass` — one carried forward, and it is in the response beside the destination rather than in the file, which is where a file-targeted run's findings belong.
  - `mechanics` — `pass` — once, in `en_GB`, finding nothing.
  - `target` — `pass` — one file at the named path; the text was not repeated in the response.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — one.
- **defects filed** — none.
- **notes** — the run says the correction budget is spent *so this finding comes back for you to finish*, which is the fourth stop condition stated at the same time as the third. Either would have ended the loop here.

## `handoff-unusable` (nothing suppresses the map)

- **fixture** — `handoff-unusable`
- **invocation** — `/redline $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a report of unusable artifact metadata: the map quoted, `en_UK` named as reaching no installed resource, the three installed resources listed, and both ways to proceed given.
- **side effects** — none.
- **criteria** —
  - `resolution` — `pass` — `en_UK` was not read as `en_GB`, and the reply says why in the Skill's own terms: that would be the run guessing at a decision the document states.
  - `refusal` — `pass` — the problem is named and the run stopped before reviewing anything.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run notes that `genre: article` and `technique: abt` in the same map are both installed, so the stop is about the one value rather than about the map.

## `handoff-unusable` (a flag supersedes the map)

- **fixture** — `handoff-unusable`
- **invocation** — `/redline --language=en_GB --max=0 $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line naming the resolved configuration and saying the map's `en_UK` had been superseded and the map now records `en_GB`, then the complete text with its frontmatter, then four unresolved findings.
- **side effects** — none.
- **criteria** —
  - `resolution` — `pass` — a `--language` value settles the parameter and suppresses the unusable-metadata stop, which is what `## Resolution` says; genre and technique still came from the map.
  - `handoff` — `pass` — the delivered artifact's map carries `article`, `abt`, `en_GB` — synchronized to what the run resolved, with the unusable value replaced rather than kept, and nothing else in the frontmatter moved.
  - `review` — `pass` — four findings on a two-paragraph text, each located and each naming what the reader loses: a title that states an outcome the body does not reach, an absolute claim the two counts under it do not carry, a throat-clearing formula, and one thing given four names.
  - `budget` — `pass` — `0`, spent nothing.
  - `mechanics` — `pass` — once, finding nothing.
  - `unresolved` — `pass` — all four, named as such.
  - `no-source` — `pass` — finding 2 says the claim cannot be repaired by supplying a source the artifact does not have, which is the correct move: it neither invents an attribution nor asks for material.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — four.
- **defects filed** — none.
- **notes** — finding 4 is the clearest example in the record of a review declining to guess: it says the fix depends on whether *the letters* are a third channel or the same material, that the text has never said which, and that the answer is the user's.

## `code-carrying`

- **fixture** — `code-carrying`
- **invocation** — `/redline --output=$RUN/out/kill-switches.md $RUN/corpus/prose/code-carrying.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/kill-switches.md`
- **observed delivery** — the reply named the destination and the resolved configuration, stated which spans it had treated as quoted material, listed six repaired findings and one unresolved one, and named the two mechanical corrections separately from the findings; the text was not repeated.
- **side effects** — `out/kill-switches.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `code` — `pass` — this is the fixture's whole question. The reply names the fenced JavaScript block, the indented block, and both inline spans as quoted material before it lists a finding, and says the *It's not just a flag*, the *Studies show*, and the misspellings inside them were read past. Nothing inside a sample produced a finding, and nothing inside one was changed.
  - `review` — `pass` — six findings on the prose layer, each located and each naming the pattern: the empty opening with its two unattributed claims, the closing that restates the opening as a rhetorical question, the false *But* with its throat-clearing and its three-part frame, the unsourced *Teams report* triplet, a false *Furthermore* carrying inflation, and a title that argues the subject matters instead of naming it.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the reply says the repairs were verified by re-review, and the unresolved finding is one the re-review raised.
  - `stop` — `pass` — the fourth condition: the budget was spent with one finding left, carried forward.
  - `mechanics` — `pass` — once, after the correction, correcting `Its a pattern` and the `enable`/`enables` agreement. The reply says explicitly that those were never findings, because *a review that lists what the mechanical pass is about to fix makes handled work look outstanding* — which is the boundary between the two passes drawn from the review's side.
  - `preserve` — `pass` — the two mechanical corrections and the six repairs are what changed; what the findings did not name came through.
  - `no-source` — `pass` — the unattributed claims were cut because the text sources neither, and nothing asks for the studies.
  - `unresolved` — `pass` — one, in the response beside the destination.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — one: the closing sentence resting on a distributed setting the rest of the text never establishes.
- **defects filed** — none.
- **notes** — the unresolved finding is about the same sentence the mechanical pass corrected for agreement, and the reply separates the two explicitly — *the finding is about the claim, not the grammar*. That is the cleanest statement in the record of what the two passes each own.

## `locale-divergent` (British English)

- **fixture** — `locale-divergent`
- **invocation** — `/redline --language=en_GB $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text, then one unresolved finding about the numeric date, then a note of the two findings that were repaired.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `en_GB` from the invocation; the mechanical pass reports checking the `licence`/`license` pair, the `£14,500` format, and the British spellings and leaving them.
  - `review` — `pass` — three findings: a restatement of paragraph 1 in the final paragraph, a passive recommendation, and the ambiguous date.
  - `budget` — `pass` — the default `1`, spent once.
  - `unresolved` — `pass` — the date is carried forward, and the reply says why it cannot be repaired here: writing `3 April` or `4 March` would assert a fact the text does not hold, and cutting it would take the note's only dated fact.
  - `mechanics` — `pass` — once, finding nothing, with the British forms named and left.
  - `preserve` — `pass` — `3/4` stands, which is the fixture's own rejection; the two repairs are the two the review named.
  - `no-source` — `pass` — nothing asks for the minute or the committee's papers.
  - `target` — `pass` — response, source untouched.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — one.
- **defects filed** — none.
- **notes** — the Proofread runs over this fixture met the same date. Under `--language=en_US` one of them rewrote it and one left it, which is #166; here, under a Skill that has somewhere to put an unresolvable observation, the run reports it as a finding instead. That is the difference a findings channel makes to the same material.

## `locale-divergent` (American English)

- **fixture** — `locale-divergent`
- **invocation** — `/redline --language=en_US $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text with the American forms applied, then two unresolved findings.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `en_US` from the invocation, and the mechanical pass applied `organized`, `judgment`, `canceling`, `specialized`, `license` for both noun and verb, and `in the fall`.
  - `review` — `pass` — two findings, both of them about what the material does not carry rather than about how it reads.
  - `budget` — `pass` — the default `1`, spent.
  - `unresolved` — `pass` — both carried forward, each with the reason it cannot be repaired from the text.
  - `preserve` — `pass` — `3/4` stands here too, and finding 2 is the reason: choosing one reading would assert a date the text does not give, and deleting it would remove the specific the sentence exists to carry.
  - `mechanics` — `pass` — once.
  - `effects` — `pass` — the inventory is identical before and after; the run reports leaving no background process behind.
- **unresolved findings** — two.
- **defects filed** — none.
- **notes** — the two locale runs applied opposite spellings to the same file and neither touched the date. Between them they are the whole of what this fixture asks of a Skill that reviews.

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/redline --output=$RUN/out/estimating.md $RUN/corpus/frontmatter/frontmatter-unrelated.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/estimating.md`
- **observed delivery** — the reply named the destination and the resolved configuration, stated that the four top-level keys are the document's own fields rather than configuration, and said one correction was delegated and verified and no findings remain.
- **side effects** — `out/estimating.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `resolution` — `pass` — `lang: fr`, `genre: fiction`, `technique: montage`, and `language: Esperanto` were all named and none was read as configuration; the genre was inferred and the language settled from the text.
  - `handoff` — `pass` — the delivered file's frontmatter is byte-identical to the source's apart from the `title` a finding named, all four bait keys preserved untouched, and no `kntnt` map was added to an artifact that had none.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the reply says the correction was verified by a fresh review.
  - `stop` — `pass` — the first condition: nothing left after the re-review.
  - `mechanics` — `pass` — once.
  - `preserve` — `pass` — the frontmatter check above is the strongest form of this criterion in the record: a Skill that edits a text and leaves an unrelated YAML block byte-identical has drawn the line exactly.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `response-default`

- **fixture** — `response-default`
- **invocation** — `/redline --max=0 $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text, unchanged, and two unresolved findings.
- **side effects** — none.
- **criteria** —
  - `target` — `pass` — no destination was named, so nothing left the response; reading a file selected nothing.
  - `effects` — `pass` — no file was created, replaced, or removed anywhere under the working copy.
  - `review` — `pass` — two findings on a two-paragraph text, each located to a sentence and each naming the contract clause it comes from: a first sentence that asserts the opposite of the argument it opens, and an unsupported absolute carrying weight.
  - `budget` — `pass` — `0`.
  - `mechanics` — `pass` — once, finding nothing.
  - `unresolved` — `pass` — both, with what would settle each.
  - `no-source` — `pass` — finding 2 says the absolute cannot be repaired by supplying evidence, since none is in the text, and that whether it holds depends on how the team works, which the review cannot settle.
- **unresolved findings** — two.
- **defects filed** — none.
- **notes** — finding 1 proposes a one-word repair and says it touches nothing else, which is the correction brief's *smallest change* rule showing up in the review rather than in the round.

## `new-file`

- **fixture** — `new-file`
- **invocation** — `/redline --max=0 --output=$RUN/out/handover.md $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/handover.md`
- **observed delivery** — the reply named the path and said there were no findings, and named two things it had considered and dismissed.
- **side effects** — `out/handover.md` created, byte-identical to the source. Nothing else.
- **criteria** —
  - `target` — `pass` — exactly that one file was created, nothing was made to hold it, and the text did not also appear in the response.
  - `effects` — `pass` — one file created, nothing else touched.
  - `review` — `pass` — nothing found in competent prose, with the reasoning for two near-misses given: the negations in paragraphs 3 and 4 correct what a reader would otherwise assume rather than knocking down positions nobody held, and the several names for the two roles are paired explicitly in the opening sentence.
  - `budget` — `pass` — `0`.
  - `mechanics` — `pass` — once, finding nothing.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — a clean run aimed at a named different file still delivers the artifact, which is what separates this entry from `clean-en-GB` above, where the same text aimed at the response returned the short status instead. Both behaviours are the delivery contract's, and the pair is what shows the distinction is being drawn.

## `existing-file`

- **fixture** — `existing-file`
- **invocation** — `/redline --max=0 --output=$RUN/corpus/output/existing-target.md $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — the reply named the destination and the resolved configuration, and listed thirteen unresolved findings ordered by what they cost the reader; the text was not repeated.
- **side effects** — `corpus/output/existing-target.md` replaced. Nothing else.
- **criteria** —
  - `target` — `pass` — the occupant was replaced without a second confirming gesture, nothing was written beside it, and the findings went to the response rather than into the file.
  - `unresolved` — `pass` — thirteen, delivered beside the destination, which is where a file-targeted run's findings belong.
  - `review` — `pass` — thirteen findings, including two the shorter reviews of this fixture did not reach: the same formula opening and closing the piece (*one thing is clear* / *One thing is certain*), and the central premise stated as settled in a text that nowhere argues for it.
  - `budget` — `pass` — `0`.
  - `mechanics` — `pass` — once, finding nothing.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
- **unresolved findings** — thirteen.
- **defects filed** — none.
- **notes** — this run and the two `slop-heavy` review-only runs above found eleven, thirteen, and thirteen findings on one text under two inferred genres. The overlap is the catalogue; the difference is what a genre asks for, and neither count is a criterion.

## `brief-article-abt` (a brief reviewed as an article)

- **fixture** — `brief-article-abt`
- **invocation** — `/redline --genre=article --technique=abt --max=0 $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete brief, unchanged, then five unresolved findings.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — and this is the entry that tests the Skill's hardest instruction. *What the artifact turns out to be is a finding and never a ground for declining to review it*, and finding 1 is exactly that, in first position: **This is a brief, not an article**, located to the whole document, with the evidence quoted — the commissioning first sentence, the audience-and-length paragraph, the *What happened.* label, and an addressee who is a writer rather than the trade reader. The run did not hand the invocation back, did not propose another Skill, and did not read another Skill's instructions to reach the judgement.
  - `technique` — `pass` — the ABT arc is judged against the material as supplied: the And is present but never established as settled, the But is the strongest thing the material holds and appears only as testimony inside a chronology, and the Therefore holds and is properly limited. That is the technique applied as a contract rather than as a checklist.
  - `budget` — `pass` — `0`.
  - `mechanics` — `pass` — once, finding nothing.
  - `no-source` — `pass` — finding 5 says the March retrospective is what would supply Miriam Adler's words and that a quotation must not be composed to close the gap. That is a finding about the artifact rather than a request for material, and it stays the right side of the line.
  - `unresolved` — `pass` — all five.
  - `preserve` — `pass` — nothing was corrected.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — five.
- **defects filed** — none.
- **notes** — the closing observation is worth keeping: the two unnamed January agents are called out as *correct rather than a gap*, because material that names nobody yields an article that names nobody. A review that had asked for their names would have been asking for source material.

## `read-only-source`

- **fixture** — `read-only-source`
- **invocation** — `/redline --in-place $RUN/corpus/output/readonly-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming the file as read-only where In-place Editing requires a writable local source, followed by the synopsis, the help pointer, and two alternatives.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — established by reading, before anything was reviewed.
  - `effects` — `pass` — the inventory is identical before and after, and the file is still mode `-r--r--r--`: no permission was changed and no result was written elsewhere as a substitute.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/redline --output=$RUN/corpus/output/in-place-source.md $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming one file as both source and destination, the synopsis, and the In-place invocation to use instead.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the refusal points at In-place Editing as the recognisable authorisation.
  - `effects` — `pass` — the file was not replaced.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/redline --output=$RUN/out/copy.md --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying the two name two destinations for one text, the synopsis, and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass`.
  - `effects` — `pass` — neither half executed: `out/copy.md` does not exist and the source is unchanged.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `url-source` (In-place Editing refused)

- **fixture** — `url-source`
- **invocation** — `/redline --in-place https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying a URL is not a writable local file and that fetching one grants no right to write anything back, the synopsis, and two alternatives.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — made by reading the invocation, before the network was touched.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `<negative Correction Budget>`

- **fixture** — none; the Skill's `## Arguments` list names it and the corpus stages no fixture for it.
- **invocation** — `/redline --max=-1 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming `-1` as negative where the budget takes only non-negative integers, followed by the synopsis and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — refused before anything was read, reviewed, or written.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `<uninstalled genre>`

- **fixture** — `slop-heavy` supplies the text; the invocation supplies the fault.
- **invocation** — `/redline --genre=listicle $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming `listicle` as not installed, listing the four that are, followed by the synopsis and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the genre was verified against what is installed and refused rather than falling back to the default.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `existing-directory`

- **fixture** — `existing-directory`
- **invocation** — `/redline --output=$RUN/out $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the derived filename, listed what the one correction round repaired, and then set out seven findings: four unresolved from the original and three the round's own repairs created.
- **side effects** — `out/slop-heavy.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `target` — `pass` — the name was derived from the source's basename and landed inside the named directory.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-review is what raised findings 5, 6, and 7.
  - `stop` — `pass` — the third condition, and this is the entry that names it most precisely: a stranded pronoun whose antecedent the repaired false contrast had supplied, two single-sentence paragraphs left by cuts, and a paragraph attached by adjacency where a false connective had been. Each is traced to the repair it followed from.
  - `preserve` — `pass` — the reply notes that the correction deliberately did not re-paragraph, since no finding concerned the paragraphing, and calls that correct while flagging the result. That is the correction brief's *repair what the findings name and nothing else* holding even where holding it leaves something untidy.
  - `unresolved` — `pass` — seven, and the reply says which four are the text's and which three are the round's.
  - `mechanics` — `pass` — once, finding nothing.
  - `no-source` — `pass`.
  - `effects` — `pass` — one file created inside the named directory.
- **unresolved findings** — seven.
- **defects filed** — none.
- **notes** — the closing sentence of the reply is the most useful thing any run in this record says about this fixture: with no material behind it, the text can be made to stop sounding generated but cannot be made to say anything. That is a judgement about the artifact rather than a finding, and it is offered as one.

## `in-place-request`

- **fixture** — `in-place-request`, with `slop-heavy` supplying the text
- **invocation** — `/redline --in-place $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place
- **observed delivery** — the reply said the source had been replaced, listed what the round repaired, and set out five unresolved findings.
- **side effects** — `corpus/prose/slop-heavy.md` replaced. Nothing else created, replaced, or removed.
- **criteria** —
  - `target` — `pass` — the source file itself received the result, no copy was left beside it, and the findings stayed in the response.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
  - `budget` — `pass` — the default `1`, spent.
  - `verify` — `pass`.
  - `stop` — `pass` — finding 4 is named as following from this run's own repair, and finding 5 is a residual the spent budget could not reach.
  - `unresolved` — `pass` — five, in the response beside the in-place destination, which is where an in-place run's findings belong.
  - `mechanics` — `pass` — once, finding nothing.
  - `no-source` — `pass`.
- **unresolved findings** — five.
- **defects filed** — none.
- **notes** — finding 4's phrasing is worth keeping: *That is the honest state of the piece rather than a new defect in it, but it is the thing to weigh before deciding whether to rebuild this text or start from the material.* A run that has cut a text to its skeleton saying so is the difference between a report and a result.

## `url-source` (reviewed, filename derived from the URL)

- **fixture** — `url-source`
- **invocation** — `/redline --max=0 --output=$RUN/out https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the derived filename and set out nine unresolved findings against RFC 2119 itself.
- **side effects** — `out/key-words-for-use-in-rfcs-to-indicate-requirement-levels.txt` created. Nothing else.
- **criteria** —
  - `target` — `pass` — the filename was derived from the URL's title rather than from any source basename, with the `.txt` extension matching the fetched text's format.
  - `budget` — `pass` — `0`.
  - `mechanics` — `pass` — once, correcting nine items, which is what `--max=0` leaves in place.
  - `review` — `pass` — nine findings on a published RFC, every one of them located to a section and turning on something inside the document: the lowercase/uppercase ambiguity in its own prose, a defined term missing from the boilerplate it tells authors to copy, four names for the thing a key word governs, an unexplained asymmetry between SHOULD and SHOULD NOT, a load-bearing qualification never defined, definitions credited to unnamed RFCs, two movements in the MAY entry, one numbering sequence carrying two kinds of thing, and a subject separated from its verb across twenty-two words.
  - `no-source` — `pass` — nothing asks for the RFCs the definitions were amalgamated from; finding 6 is that the document does not name them, which is a defect visible inside the artifact.
  - `unresolved` — `pass` — all nine.
  - `effects` — `pass` — one file created inside the named directory.
- **unresolved findings** — nine.
- **defects filed** — none.
- **notes** — this is the only run in the record whose material came over the network, and the one that most clearly shows the review reading a text nobody in this collection wrote.

## `factual-source-long`

- **fixture** — `factual-source-long`
- **invocation** — `/redline --genre=report --max=0 $RUN/corpus/source/factual-source-long.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text, unchanged, then eight unresolved findings.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — eight findings against the report contract, the first of which is the same move `brief-article-abt` calls for: this is source material rather than a report, and the document says so itself in its own provenance line and its own closing heading. It is a finding rather than a refusal to review.
  - `no-source` — `pass` — every finding turns on something inside the artifact; nothing asks for the operator's report, the committee's minutes, or the survey instrument, and where a finding cannot be closed the reply says which document would close it rather than requesting one.
  - `budget` — `pass` — `0`.
  - `mechanics` — `pass` — once, finding nothing.
  - `unresolved` — `pass` — all eight.
  - `preserve` — `pass` — nothing was corrected.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — eight.
- **defects filed** — none.
- **notes** — finding 3 is an arithmetic contradiction inside the fixture: the 2024 breakdown of 312,000 weekday, 63,000 Saturday, and 18,400 Sunday boardings sums to 393,400 against a stated total of 412,000, while the 2023 pair reconciles to within rounding. That is a fact about the corpus rather than about this Skill, and it is recorded here rather than filed, because nothing in the corpus says whether the gap is planted for a review to find or is an oversight. It is worth a later reader's attention either way: the Write record for the same date shows a draft that used both figures without noticing.

## `interview-transcript`

- **fixture** — `interview-transcript`
- **invocation** — `/redline --max=0 $RUN/corpus/source/interview-transcript.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete transcript, unchanged, then four unresolved findings.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — the first finding settles what the artifact is, quoting its own header — *Transcribed as spoken, including fillers and repetition* — and says that most of the document is a failure by design, that the disfluency is the fidelity of the record, and that cutting it would leave a document that no longer is what its header says. The other three concern the transcriber's prose and the record's integrity rather than the speaker's words: a date with no year, no named interviewer or transcriber and no statement of completeness, and the framing note running into the record with nothing marking the join.
  - `preserve` — `pass` — nothing was corrected, and `--max=0` is why; but the review's own reasoning is what matters here, since it identifies the passages a correction round would have been wrong to touch before any round could touch them.
  - `budget` — `pass` — `0`.
  - `mechanics` — `pass` — once, finding nothing.
  - `no-source` — `pass` — the missing year and the missing provenance are named as unresolvable from the material rather than requested.
  - `unresolved` — `pass` — all four.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — four.
- **defects filed** — none.
- **notes** — the corpus stages this fixture for Write's quotation invariant. Reviewed as an artifact it stages something else, and the run found it: a text whose apparent defects belong to the speaker and not to a writer. Finding 4 — the only one a correction round could have repaired without inventing anything — is the one that is genuinely the transcriber's.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/redline --genre=article --output=$RUN/out/felanmalan.md $RUN/corpus/frontmatter/handoff-conflicting.md -- Behandla den som svensk text.`
- **contextual instruction** — `Behandla den som svensk text.`
- **output target** — `$RUN/out/felanmalan.md`
- **observed delivery** — a Swedish reply naming the path and setting out the resolution per field, saying the Contextual Instruction had nothing left to settle and was therefore not applied, and listing three unresolved findings.
- **side effects** — `out/felanmalan.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `resolution` — `pass` — three parameters settled at three levels in one invocation: `article` from the Formal Invocation, `pac` and `en_US` from the map. The instruction naming Swedish sits below the map in the precedence and was suppressed rather than refused, and the reply says so and says which gesture would have won instead. That is per-field precedence and suppression both, in one run.
  - `handoff` — `pass` — the delivered map is synchronized to what the run resolved: `genre` moved from `report` to `article`, `technique` and `language` unchanged because the map is where they came from. Nothing else in the frontmatter moved, and the source file is untouched.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-review of the repaired text raised two new findings.
  - `stop` — `pass` — the third condition, and both new findings are traced to the same repair: the correction inserted the missing PAC premise in two places rather than one, and closed the piece on a restatement of its own figures.
  - `unresolved` — `pass` — three, in the response beside the destination.
  - `mechanics` — `pass` — once, in `en_US`, finding nothing.
  - `no-source` — `pass`.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — three.
- **defects filed** — none.
- **notes** — finding 3 is the most interesting thing the fixture produced. The run reports that a map declaring `en_US` over Swedish prose *decided the review*: the American review and anti-slop guidance had nothing to bite on, and the mechanical pass ran on `en_US` against Swedish sentences and found nothing. It names the contradiction as the user's to settle rather than resolving it, which is right — the precedence gave the map the language, and a run that overrode it on the evidence of the prose would be inferring past a value the artifact states. What the entry records is that obeying the precedence here costs the review its language-specific half, and that the run said so.

## `handoff-partial`

- **fixture** — `handoff-partial`
- **invocation** — `/redline --genre=report --output=$RUN/out/nyhetsbrev.md $RUN/corpus/frontmatter/handoff-partial.md -- The language is Swedish.`
- **contextual instruction** — `The language is Swedish.`
- **output target** — `$RUN/out/nyhetsbrev.md`
- **observed delivery** — a Swedish reply naming the path, naming the three levels that settled the three parameters, listing what the round repaired, and setting out four unresolved findings.
- **side effects** — `out/nyhetsbrev.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `resolution` — `pass` — the fixture's whole question, answered: the invocation settled the genre, the map settled the technique, and the Contextual Instruction settled the language the map leaves absent and the text cannot supply. Three levels, one invocation, one parameter each.
  - `handoff` — `pass` — the delivered map carries `report`, `abt`, `sv`: the technique the map already held, plus the two values it did not, synchronized to what the run resolved. Nothing else in the frontmatter moved.
  - `review` — `pass` — six findings on the first pass, including the language alternation inside sentences, the report's answer arriving last, and the numbers without their basis.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-review raised findings 3 and 4.
  - `stop` — `pass` — the fourth condition, with the third also named: the budget was spent, and two of the four remaining findings are the round's own.
  - `unresolved` — `pass` — four, each with what would settle it.
  - `mechanics` — `pass` — once, in Swedish, finding nothing.
  - `no-source` — `pass` — finding 1 says the missing figures must come from the underlying material and cannot be filled in without inventing them.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — four.
- **defects filed** — none.
- **notes** — the two absent keys were never read as a reason to stop or to ask for a complete map, which is the fixture's first rejection. The round also translated the text's English passages into Swedish under finding 1, which is a large repair — but it is the repair the finding named, and the finding is the one the resolved language makes unavoidable.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/redline $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text alone, with no findings beside it.
- **side effects** — none.
- **criteria** —
  - `handoff` — `pass` — the artifact carries no `kntnt` map and none was added, which is what the Skill's `## Resolution` requires of a text that has none.
  - `budget` — `pass` — the default `1`, spent once.
  - `stop` — `pass` — the first condition: the re-review found nothing, so the loop stopped with nothing to carry.
  - `unresolved` — `pass` — none, and the delivery is therefore the Text Artifact alone, which is exactly what step 11 asks for where no findings remain.
  - `preserve` — `pass` — the repairs are the two the review named: the superlative closing claim, cut; and the drift between *roster* and *rota*, settled on one word. Everything else is as it arrived.
  - `mechanics` — `pass` — once.
  - `target` — `pass` — response, and the source is byte-identical to the corpus.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the only entry in the record whose delivery carries no findings at all, and it is worth having: a run that resolved everything says nothing about the review, because there is nothing left to say. The earlier attempt at this invocation is recorded under **Runs discarded**.

## `slop-heavy-sv` (language named, one correction)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/redline --language=sv --max=1 $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish reply naming the resolved configuration, the corrected text, and eight unresolved findings.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `sv` from the invocation, and the whole report in Swedish.
  - `review` — `pass` — the first review found the Swedish patterns as the `--max=0` run did, and the re-review found eight things standing.
  - `budget` — `pass` — `1`, spent once.
  - `verify` — `pass` — the reply says explicitly that the returned text was re-read from the top rather than accepted on its own report.
  - `stop` — `pass` — the fourth condition, with two of the eight named as the round's own: finding 5 is one the first review missed and the round therefore never saw, and finding 8 is a claim the correction created by welding two sentences the original kept apart.
  - `unresolved` — `pass` — all eight, each with what it would take to settle it.
  - `mechanics` — `pass` — once, in Swedish, after the correction.
  - `no-source` — `pass` — finding 2 says the unattributed authorities were cut because they could not be repaired without inventing a source.
  - `preserve` — `pass` — `Service & support` and the `”kundresa”` quotation marks survive into the delivered text, so the mechanical pass corrected what it owns and the review did not reach past its own findings.
  - `effects` — `pass` — the inventory is identical before and after; the source file is untouched.
- **unresolved findings** — eight.
- **defects filed** — none.
- **notes** — finding 5 is unusually candid: the run says the item *missades i den första granskningen och kom därför aldrig med i korrigeringsrundan*. A review reporting what its own first pass missed is the loop working as designed — the re-review is a fresh reading of the text in front of it rather than a check of the round's homework, and this is what that difference buys.

## `code-carrying-sv`

- **fixture** — `code-carrying-sv`
- **invocation** — `/redline --output=$RUN/out/avstangning.md $RUN/corpus/prose/code-carrying-sv.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/avstangning.md`
- **observed delivery** — a Swedish reply naming the path and the resolved configuration, listing eight repaired findings and the four mechanical corrections separately, and setting out four unresolved findings.
- **side effects** — `out/avstangning.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `code` — `pass` — verified on disk: the fenced Python block and the indented block hash identically to the fixture's, and `emmot`, `seperat uppdaterings loop`, the docstring's patterns, and the inline spans `nyckeln_till_framgang.ttl` and `emmottagen_tid` are all untouched. The reply says as much before it lists anything, naming the comment, the docstring, and the error string as full of the same patterns the prose was criticised for and read past all the same.
  - `language` — `pass` — Swedish inferred, and the report is in Swedish.
  - `review` — `pass` — eight findings on the prose layer, the Swedish patterns among them.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-review raised findings 1 and 2.
  - `stop` — `pass` — the third condition, and the reply names it: *Punkt 1 och 2 är följder av rundans egna strykningar, inte av originalet.*
  - `mechanics` — `pass` — once, after the correction, correcting the four planted prose errors and nothing inside the code.
  - `preserve` — `pass` — `Drift & utveckling` is on disk with its literal ampersand, and finding 4 is the review declining to change it: the text does not say whether it is a department's proper name, so it was left and named.
  - `unresolved` — `pass` — four, in the response beside the destination.
  - `no-source` — `pass`.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — four.
- **defects filed** — none.
- **notes** — this and `code-carrying` are the two entries whose code claim is checked against bytes rather than against a transcript, and both hold.

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/redline --max=0 --output=$RUN/corpus/output/collision $RUN/corpus/output/interview-notes.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the reply named the resolved configuration and the derived filename, said the two files already in the directory were untouched, and set out five unresolved findings.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants and the source are byte-unchanged.
- **criteria** —
  - `target` — `pass` — the stem stayed `interview-notes` and the first free candidate in ascending order was taken; `interview-notes-2-2.md`, the name the corpus names as the wrong answer, was not written.
  - `budget` — `pass` — `0`, spent nothing.
  - `mechanics` — `pass` — once, finding nothing, so the delivered file is byte-identical to the source.
  - `review` — `pass` — five findings, and finding 2 is the one worth keeping: attribution applied unevenly in a record of an interview, where two statements are credited to Halldin and three are asserted in the document's own voice, so the reader cannot tell which are her account.
  - `no-source` — `pass` — finding 5 says settling it needs what Halldin actually said, which the text does not carry. That names the material without asking for it.
  - `unresolved` — `pass` — five, in the response beside the destination.
  - `effects` — `pass` — one file created, neither occupant overwritten.
- **unresolved findings** — five.
- **defects filed** — none.
- **notes** — the same fixture under Write and under Unslop produced the same derived name, which is the delivery contract behaving identically across three Skills that reach it by three different routes.

## Fixtures deliberately skipped

Three fixtures were not run against this Skill. Each is recorded here rather than omitted, because a record silently missing a fixture reads later as a fixture that passed.

- `brief-short` — `skipped` — a hundred-word brief whose rejection judges a draft's supported facts. Reviewed as an artifact it would stage what `brief-article-abt` already stages and stages harder: a document that is a brief rather than the genre it is held to. Running it would add a second instance of one finding and nothing else.
- `brief-report-pac` — `skipped` — same reason. Its rejection is about a draft resolving a counter-argument by inventing evidence, which belongs to the Skill that writes; the report genre and the PAC technique are both exercised here by `handoff-partial` and `handoff-conflicting`, which take them from a map and an invocation respectively.
- `brief-press-release-sv` — `skipped` — same reason, and the press-release genre is the one installed genre no run in this record resolved. That is a genuine gap and it is named as one: nothing here establishes how the review reads a text against that contract. The Swedish half of what it would have added is covered by `slop-heavy-sv`, `code-carrying-sv`, `flawed-sv`, `handoff-partial`, and `handoff-conflicting`.

## What this record establishes, and what it does not

Thirty-seven fixture runs. Thirty-six are clean; one carries a failing criterion.

The failure is on `flawed-en-US`, where the correction round removed a fact along with the defect wrapped around it, in a case the Skill's own correction brief legislates for and where the smaller repair was available and obvious. That is filed as #179.

The loop is the thing this Skill is built around, and the runs exercise all four of its stopping conditions. It stopped clean with budget unspent on `clean-en-GB`, `flawed-sv`, `resembles-abt`, `frontmatter-unrelated`, and `frontmatter-absent`. It stopped on the budget with findings left on `code-carrying`, `handoff-partial`, and `slop-heavy-sv`. And it stopped on a finding a round's own repair created — the condition that is hardest to see from inside a loop and that only the outer run can see at all — on `slop-heavy` at three separate budgets, on `handoff-present`, on `handoff-conflicting`, on `existing-directory`, on `in-place-request`, and on `code-carrying-sv`. Every one of those runs named the repair the new finding followed from, which is what makes the stop a report rather than an abandonment.

`no-source` holds without exception across thirty-six runs, including on the three fixtures supplied with no material at all and on the two that are source material for something else. Where a finding could not be closed from the artifact, the runs said which document would close it; not one asked for material, and not one remarked that source verification was unavailable.

The anti-slop catalogue reached both shipped languages. `slop-heavy-sv` under review-only produced fourteen findings naming the Swedish empty openings, the imported false contrast, the metaphor stock as a set, superlative inflation, the wholesale-translated hedges, the triad reflex, the synonym cycling, and the empty attributions — from a catalogue written in English and applied by what each pattern does.

Both code fixtures came back with every fenced block, indented block, and inline span byte-identical, verified on disk, with the misspellings and the split compound inside them uncorrected and no finding located in one.

What this record does not establish: anything about the press-release genre, which no run resolved; anything about the Skill under a Harness other than Claude Code; and anything about the ordinary slash-command path, since `disable-model-invocation` makes it unreachable from a sub-session and the **Run conditions** describe what was used instead.

One observation about the corpus rather than the Skill is recorded on the `factual-source-long` entry: the fixture's 2024 boarding breakdown does not sum to its stated 2024 total, while the 2023 pair reconciles. Whether that is planted for a review to find or is an oversight, the corpus does not say, so it is noted rather than filed.

## Runs discarded

**Five runs blocked by this session's own concurrency ceiling.** Redline delegates each correction to a fresh subagent. This session drives its runs as sub-sessions, so a correction subagent is a nested one, and the Harness caps concurrent subagents at twenty for the session as a whole. Five runs with a positive budget reached the correction step while that cap was full, were refused a subagent, and correctly declined both to correct the text themselves and to pretend the budget had been spent — each reported that no round had run, carried every finding forward as unresolved, and named the cap as the reason. Those five are `slop-heavy` to a named file, `slop-heavy-sv` with the language named, `handoff-conflicting`, `handoff-partial`, and `frontmatter-absent`.

They are discarded rather than recorded because what they observe is this session's dispatch policy, not the Skill: a user typing `/redline` has no twenty other sub-sessions competing for the pool. Each was re-run from a fresh working copy once capacity was free, and it is those re-runs the record holds. The behaviour under the constraint is worth one sentence all the same, since it is the Skill's own: told it could not start a fresh subagent, it did not repair its own findings, which is the one thing the loop exists to prevent.
