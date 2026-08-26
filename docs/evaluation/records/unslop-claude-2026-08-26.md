# unslop — claude — 2026-08-26

- **record** — `unslop-claude-2026-08-26`
- **date** — `2026-08-26`
- **ticket** — `#162`
- **skill** — `unslop`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.246
- **corpus commit** — `46ba9c1`

## Run conditions

The Skill was run against the copy installed at `~/.claude/skills/unslop`. `diff -r` reported that directory byte-identical to `skills/editorial/unslop/` at the corpus commit, and the same for `~/.claude/skills/kntnt/` against `skills/kntnt/`, the Manager and the Collection Library it resolves through, with no difference but the untracked `__pycache__` directories the repository working tree carries and an installed copy does not. Unslop declares no peer Skill — it runs no mechanical pass and selects no editorial contract — so the Manager and its Library are the whole of its dependencies.

Each fixture ran in a Claude Code agent session of its own, started from this session, with no memory of any other run and no access to this repository's evaluation material: the turn carried the invocation and nothing else, and no run was given the ticket or the criteria below. Each ran in its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says — `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form.

**side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself.

**How the Skill was started.** Unslop carries `disable-model-invocation: true`, so the Skill tool refuses to start it from inside a turn and a sub-session never receives an expanded slash command. Each run was therefore handed what the Harness itself gives a user-invoked Skill: the installed `SKILL.md` named as the turn's instructions, with `$HERE` named as the directory holding it. The run read that file from disk and followed it, including the checker it runs, the resolver it runs, the references it loads, and the correction subagents it starts. The Write record for the same date sets the reasoning out in full.

Judging was done from the delivered reply and the filesystem inventory alone, against the criteria below, fixture by fixture, before any GPT-family record existed to compare with. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

The criterion identifiers are stable across entries: `catch` (the catalogue's patterns are found where the fixture plants them, named rather than disliked), `lens` (nothing outside the anti-slop lens is corrected — mechanics stay, and no genre, technique, or structural expectation is imposed), `no-mechanics` (no mechanical pass is invoked at the end of any run), `budget` (the Correction Budget is a ceiling spent as the shared loop contract says), `fresh` (each correction goes to a subagent started fresh with the complete current text and findings), `verify` (a correction is verified by a fresh reading rather than accepted on its own report), `stop` (the loop stops at one of the four conditions and says which), `unresolved` (findings left over are delivered with the artifact and named as unresolved), `language` (the resolved language is the one the precedence names), `handoff` (a recognized map supplies the language and is neither created, synchronized, nor otherwise disturbed), `preserve` (material outside the findings comes through untouched), `code` (a code sample produces no finding and comes back byte for byte), `no-source` (no source-verification commentary anywhere), `status` (the short no-change status where the contract asks for one), `target` (the artifact went where the output contract sends it), `effects` (the filesystem shows what the contract allows and nothing else), and `refusal` (a refused invocation names the problem, prints the synopsis, points at help, and leaves nothing behind).

## `slop-heavy` (review only, budget zero)

- **fixture** — `slop-heavy`
- **invocation** — `/unslop --max=0 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text, unchanged, then eighteen findings located paragraph by paragraph, each labelled with the pattern it is; and a closing line saying spelling, punctuation, and grammar were not examined and that `/proofread` is the gesture for those.
- **side effects** — none.
- **criteria** —
  - `catch` — `pass` — all seven patterns found and named: the empty opening and two more empty openings inside the text, four false contrasts quoted in full, importance inflation itemised from the title down, two vague attributions in the paragraph that looks most like evidence plus *The benefits are numerous and well-documented*, three robotic-rhythm paragraphs, the generic conclusion, and the four names for one subject. Every finding carries the pattern's name.
  - `lens` — `pass` — no genre is named or implied anywhere, no technique, and no structural expectation; the reply never asks what kind of text this is.
  - `no-mechanics` — `pass` — the reply says the mechanical layer was not examined and points at the other Skill for it.
  - `budget` — `pass` — `0`, spent nothing, no subagent started.
  - `unresolved` — `pass` — all eighteen, named as such.
  - `preserve` — `pass` — the text came back as it arrived.
  - `no-source` — `pass` — the two unattributed claims are named as unattributed and the reply says a real citation would have to come from the author; nothing asks for the studies.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — eighteen.
- **defects filed** — none.
- **notes** — the finding on *a significant portion* is the sharpest in the set: the reply says the phrase withholds the number that would make the claim worth stating, which is the vague-attribution pattern read for what it costs rather than for how it sounds.

## `slop-heavy` (default budget)

- **fixture** — `slop-heavy`
- **invocation** — `/unslop $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text, then two unresolved findings and a paragraph headed *What you have to settle*.
- **side effects** — none.
- **criteria** —
  - `catch` — `pass` — eighteen on the first pass.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the reply says the result was re-read from the top, and the two findings it carries come from that reading.
  - `stop` — `pass` — the third condition, named: both new findings follow from the repair rather than from the original, so the loop stopped rather than correcting its own work.
  - `unresolved` — `pass` — two, each traced to the cut it followed from.
  - `no-mechanics` — `pass` — *Nothing mechanical was touched* is the reply's own closing line.
  - `lens` — `pass` — nothing about genre, arrangement, or what the text is for.
  - `no-source` — `pass` — the unsourced claims were cut rather than sent back for sources, and the reply says that restoring them with real attribution is the user's to do if the material exists.
  - `target` — `pass` — response, and the source is byte-identical to the corpus.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — two.
- **defects filed** — none.
- **notes** — the corrected text is five short paragraphs from six long ones. The reply's account of why is the right one: the catalogue removes an unsourced claim rather than dressing it, and this draft's length was largely claims of that kind.

## `slop-heavy` (budget of three)

- **fixture** — `slop-heavy`
- **invocation** — `/unslop --max=3 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text, then three unresolved findings, and a closing paragraph on what the pass exposed.
- **side effects** — none.
- **criteria** —
  - `budget` — `pass` — three available, one spent, two unspent, and the reply says the loop stopped early rather than running the number out.
  - `stop` — `pass` — the third condition again, and this entry is where it costs the most: two rounds were still available and were deliberately not taken.
  - `catch` — `pass` — eighteen on arrival, seventeen repaired.
  - `verify` — `pass` — the re-reading is what produced the three.
  - `no-mechanics` — `pass` — stated explicitly.
  - `unresolved` — `pass` — three, and finding 3 says why it cannot be repaired: making the claim concrete would mean inventing a figure, and cutting it would take the piece's central claim.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — three.
- **defects filed** — none.
- **notes** — the closing advice is the useful half of a bounded loop: *repairing the rhythm of five sentences you may be about to replace is work spent twice.* A run that has spent one of three corrections and stopped, saying why the other two would be wasted, is the budget behaving as a ceiling rather than a quota.

## `slop-heavy-sv` (review only, language inferred)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/unslop --max=0 $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text, unchanged, then twenty-eight findings in Swedish, grouped by paragraph and each labelled with its pattern.
- **side effects** — none.
- **criteria** —
  - `catch` — `pass` — the strongest single result in the record. The catalogue is written in English and was applied by what each pattern does: the Swedish empty openings by name, the imported false contrast three times, the metaphor stock as a set, superlative inflation, five wholesale-translated hedges in one paragraph, the triad reflex with both triads quoted, synonym cycling across five names for one thing, the mechanical rhythm of two paragraphs, three empty attributions, the generic closing with its four stacked formulas — and, separately, the items the Swedish scope names that English has no counterpart for: the unspaced em dash, the curly English quotation marks, the serial comma inside a Swedish list, `&` for *och*, and the comma after a fronted connective adverb.
  - `language` — `pass` — Swedish inferred, and the whole report is in Swedish.
  - `no-mechanics` — `pass` — and this is the entry that proves it: the delivered text still carries `snabbare—det`, `Dessutom,`, `“kundresa”`, the serial comma, and `&`. Every one of them is reported as a finding and not one is corrected. The paired Redline and Proofread records show the same five items being *corrected* by a mechanical pass; here they are found and left, which is the boundary drawn from the other side.
  - `lens` — `pass` — no genre, no technique, no structural expectation.
  - `budget` — `pass` — `0`.
  - `preserve` — `pass` — the text is byte-identical to the fixture.
  - `unresolved` — `pass` — all twenty-eight.
  - `no-source` — `pass` — the three unattributed authorities are named, with the instruction not to invent a source to fill the gap.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — twenty-eight.
- **defects filed** — none.
- **notes** — twenty-eight findings against the eighteen the English fixture produced, on a text of comparable length. The difference is the Swedish scope's own items, which have no English counterpart, and it is what the fixture exists to show.

## `slop-heavy-sv` (language named, one correction)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/unslop --language=sv --max=1 $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text, then three unresolved findings and a paragraph on what was removed and may need deciding about.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `sv` from the invocation.
  - `catch` — `pass` — twenty-eight on arrival, across all seven patterns plus the Swedish tells.
  - `budget` — `pass` — `1`, spent once.
  - `verify` — `pass` — the reply says the result was re-read from the top.
  - `stop` — `pass` — the third condition, and all three findings are traced to the repair that produced them: two are halves of false contrasts left standing alone once the rejected half was cut, and the third is the rhythm of what remains.
  - `no-mechanics` — `pass` — stated, and the delivered text still carries `”kundresa”` corrected to the Swedish pair by nobody — the quotation marks in the delivered text are the Swedish ones only because the correction round rewrote that sentence, not because a mechanical pass ran.
  - `unresolved` — `pass` — three.
  - `no-source` — `pass` — the four unattributed claims are listed by name, with the catalogue's rule stated: the repair for an unsourced claim is to cut it, never to invent a source.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — three.
- **defects filed** — none.
- **notes** — findings 1 and 2 are the same shape as the English fixture's, and for the same reason: reducing a false contrast to its second half is the catalogue's repair, and the surviving half sometimes turns out to be an empty opening or a bare claim on its own. That is the loop finding what the loop is for.

## `clean-en-GB`

- **fixture** — `clean-en-GB`
- **invocation** — `/unslop $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence: the text reads clean against the catalogue in British English, nothing was written, and the budget went unspent.
- **side effects** — none.
- **criteria** —
  - `catch` — `pass` — nothing found in prose the corpus built to be competent, and nothing proposed.
  - `status` — `pass` — the short no-change status rather than a rewritten text, which is what the contract asks of a clean response-targeted run.
  - `budget` — `pass` — the default `1`, unspent.
  - `stop` — `pass` — the first condition.
  - `no-mechanics` — `pass`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `flawed-en-US`

- **fixture** — `flawed-en-US`
- **invocation** — `/unslop --max=0 $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a short status: no findings, the file not modified, and one sentence saying the mechanical layer is `/proofread`'s gesture and not this one's.
- **side effects** — none.
- **criteria** —
  - `lens` — `pass` — this is the entry the criterion exists for. The fixture is dense with mechanical errors and the pass reports none of them, because none is an anti-slop pattern.
  - `catch` — `pass` — nothing found, and the reply names the two places that come closest and says why each is doing real work: the negative-positive sentence corrects what the reader has just been led to believe, and the closing paragraph makes a new point rather than summarising.
  - `no-mechanics` — `pass` — explicit.
  - `preserve` — `pass` — the file is untouched.
  - `budget` — `pass` — `0`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — a pass that found nothing here and eighteen things in `slop-heavy` is the clearest demonstration in the record that the lens is a lens rather than a general dislike of prose.

## `flawed-sv`

- **fixture** — `flawed-sv`
- **invocation** — `/unslop --max=0 $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a short Swedish status: no anti-slop findings, nothing changed, nothing written.
- **side effects** — none.
- **criteria** —
  - `lens` — `pass` — the Swedish counterpart of the entry above: the fixture's six planted mechanical errors are all still there and none is reported.
  - `catch` — `pass` — nothing found, and the reply says what it checked: the text opens on a fact, keeps one name for the metric, varies its sentence shapes, attributes its turning point to a concrete event rather than to *studier visar*, carries no inflation or stock metaphors, and closes on a new point.
  - `language` — `pass` — Swedish inferred, and the status is in Swedish.
  - `no-mechanics` — `pass` — the reply says the remaining faults are mechanical and that this pass does not touch them.
  - `status` — `pass` — the short status.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `code-carrying`

- **fixture** — `code-carrying`
- **invocation** — `/unslop --output=$RUN/out/kill-switches.md $RUN/corpus/prose/code-carrying.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/kill-switches.md`
- **observed delivery** — the reply named the destination, said one correction was delegated and the result read again from the top with nothing left, and closed by saying spelling, grammar, and punctuation were left as they arrived.
- **side effects** — `out/kill-switches.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `code` — `pass` — verified on disk: the fenced JavaScript block and the indented block hash identically to the fixture's, and `recieved` survives in both the thrown message and the inline span, as does `seperate` in the indented block's comment. No finding was located in a sample and nothing inside one was changed.
  - `lens` — `pass` — verified on disk against the fixture's three planted prose mechanics: `Its a pattern` and the `enable` subject-verb disagreement are both still in the delivered file. The duplicated `can can` is gone, but not corrected — the whole clause it sat in (*fostering a culture of confidence where every engineer can can act*) was cut as importance inflation, so the duplication left with the finding rather than being repaired as an error. `enable`, four words earlier in the same sentence, is the proof: a pass doing mechanics would have taken it.
  - `catch` — `pass` — the diff shows what the round repaired: the empty opening with its two unattributed claims, the false-`But` paragraph with its throat-clearing and three-part frame, the unsourced *Teams report* triplet, the inflated trailing clause, the generic closing, and the title.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-reading found nothing left.
  - `stop` — `pass` — the first condition.
  - `no-mechanics` — `pass` — stated, and demonstrated by the file.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the `lens` check here is the most exacting in the record, because the fixture puts a mechanical error inside a passage an anti-slop finding removes. What separates the two is the sentence that survived: the pass cut what it found and left what it does not own.

## `code-carrying-sv`

- **fixture** — `code-carrying-sv`
- **invocation** — `/unslop --output=$RUN/out/avstangning.md $RUN/corpus/prose/code-carrying-sv.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/avstangning.md`
- **observed delivery** — a Swedish reply naming the destination, listing thirteen findings the round repaired, stating that the code came back byte for byte however much it sounds like the prose around it, and carrying one unresolved finding.
- **side effects** — `out/avstangning.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `code` — `pass` — verified on disk: the fenced Python block and the indented block hash identically to the fixture's, `emmot` and `seperat uppdaterings loop` are untouched, and the inline spans are unedited.
  - `lens` — `pass` — verified on disk: all four planted Swedish prose mechanics — `dem svåra`, `uptäckte`, `om om`, and `drift instruktion` — are still in the delivered file. The reply says so and points at `/proofread`.
  - `catch` — `pass` — thirteen findings including the Swedish tells: the em dash, the `Dessutom,` comma, the triad reflex, and `&` for *och*, all repaired as anti-slop items rather than as mechanics.
  - `language` — `pass` — Swedish inferred, report in Swedish.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the unresolved finding was raised by the re-reading of the corrected text.
  - `stop` — `pass` — the fourth condition: the budget was spent with one finding left.
  - `no-mechanics` — `pass`.
  - `unresolved` — `pass` — one, with the reason it cannot be repaired: naming who reports, or cutting the sentence, and a likely source is not invented.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — one.
- **defects filed** — none.
- **notes** — the unresolved finding is a vague attribution the correction round created by condensing three *Teamen rapporterar* sentences into one. The pattern survived its own repair, and the re-reading caught it — which is what the re-reading is for.

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/unslop $RUN/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence: no anti-slop findings, the text needed no changes, nothing was written.
- **side effects** — none.
- **criteria** —
  - `lens` — `pass` — no technique was resolved, reported, or acted on; this Skill selects none, and the reply names none. The text's *But* and *Therefore* produced no false-contrast finding.
  - `catch` — `pass` — nothing found in competent prose.
  - `status` — `pass` — the short no-change status.
  - `budget` — `pass` — the default `1`, unspent.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the fixture's rejection is about a technique reported or acted on where nothing selected it. Unslop has no technique parameter at all, so it passes by construction; what the entry establishes instead is that the text's ABT shape did not read as the false-contrast pattern.

## `mixed-language`

- **fixture** — `mixed-language`
- **invocation** — `/unslop $RUN/corpus/prose/mixed-language.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one question and nothing else: the reply quoted two code-switching sentences, walked the precedence out loud, named the three installed candidates, and said nothing had been read against the rules and nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the language was asked about before the pass rather than guessed.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none; nothing was reviewed.
- **defects filed** — none.
- **notes** — the reply adds one thing worth having: code-switching is not itself an anti-slop pattern, so the mixing will come through untouched whichever language is named. That tells the user what their answer does and does not change.

## `locale-divergent`

- **fixture** — `locale-divergent`
- **invocation** — `/unslop --language=en_GB --max=0 $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence: the text is clean against the catalogue and the British English guidance, nothing changed, nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `en_GB` from the invocation.
  - `lens` — `pass` — the fixture's whole point for a mechanical pass is its locale-divergent forms, and none of them produced a finding here; `3/4`, `£14,500`, `licence`, and the quotation placement are all untouched and unremarked.
  - `catch` — `pass` — nothing found.
  - `status` — `pass` — the short status.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus stages this fixture for locale mechanics. Under a Skill with no mechanics scope it stages the absence of them, and that is what it got.

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/unslop --max=0 --output=$RUN/out/archive.md $RUN/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/archive.md`
- **observed delivery** — the reply named the destination, said the language came from the `language: en_GB` value in the text's own `kntnt` map, reported no findings with the reasoning for the closest near-miss, and said the map was read for its language and left exactly where it was.
- **side effects** — `out/archive.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `handoff` — `pass` — this is the criterion the fixture is here for, and the file on disk settles it: the delivered artifact is byte-identical to the source, `kntnt` map and all. The map supplied the language and was neither created, synchronized, nor otherwise disturbed — which is exactly where this Skill differs from Redline, whose step 8 synchronizes the same map.
  - `language` — `pass` — from the map, the second level of the precedence.
  - `catch` — `pass` — nothing found, with the reasoning given: the third paragraph's *not whether … it is whether* is a live correction of what a reader coming off a 60 per cent rise would otherwise assume, not a false contrast.
  - `lens` — `pass` — the map's `genre: article` and `technique: abt` were read past; nothing in the reply resolves or applies either.
  - `budget` — `pass` — `0`.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the map carries three keys and this Skill has one parameter. Reading the one and leaving the other two alone, in a file it then wrote out unchanged, is the whole of what the fixture asks.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/unslop --max=0 $RUN/corpus/frontmatter/handoff-conflicting.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish status saying nothing needed changing, followed by a note that the language resolved to `en_US` from the map, that the text is Swedish, and that the pass was therefore read against American English guidance — with the gesture that would change it.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the map beat inference from the text, which is the precedence working; the run named the consequence rather than overriding the map on the evidence of the prose.
  - `handoff` — `pass` — nothing was written, so nothing was disturbed; the map is untouched.
  - `catch` — `pass` — nothing found.
  - `status` — `pass` — the short status.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the Redline record's entry for the same fixture reports the same thing and calls it what it is: a map declaring `en_US` over Swedish prose decides the review, and the language-specific half of the pass then has nothing to bite on. Here that shows as a clean result on a text the Swedish scope would have had items for, and the run said so instead of quietly returning nothing.

## `handoff-partial`

- **fixture** — `handoff-partial`
- **invocation** — `/unslop --max=0 $RUN/corpus/frontmatter/handoff-partial.md -- The language is Swedish.`
- **contextual instruction** — `The language is Swedish.`
- **output target** — `response`
- **observed delivery** — a Swedish status naming the seven patterns it had checked and found none of.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the map carries only `technique`, so the language fell through to the Contextual Instruction, which is the third level and the one this fixture stages.
  - `handoff` — `pass` — the map's `technique: abt` was read past rather than acted on, and nothing was written, so the map is untouched.
  - `lens` — `pass` — no technique resolved and none applied.
  - `status` — `pass` — the short status, in the artifact's resolved language.
  - `catch` — `pass` — nothing found.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the incomplete map was never read as a reason to stop or to ask for a complete one, which is the fixture's first rejection.

## `handoff-unusable`

- **fixture** — `handoff-unusable`
- **invocation** — `/unslop $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a report of unusable artifact metadata: the value quoted, the three installed resources named, an explicit statement that `en_UK` is not reinterpreted however close the spelling looks, and both ways to proceed.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `en_UK` was not read as `en_GB`, and the run stopped before reading the text against anything.
  - `refusal` — `pass` — the problem is named and nothing was read or written.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the reply's phrasing is the right one: a value that resembles a code is not the code, and reading it as the nearest match would settle a configuration the file never stated.

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/unslop --output=$RUN/out/estimating.md $RUN/corpus/frontmatter/frontmatter-unrelated.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/estimating.md`
- **observed delivery** — the reply named the destination, said the four top-level keys are the document's own and not this collection's configuration, and reported one finding repaired and nothing left.
- **side effects** — `out/estimating.md` created. The source is byte-identical to the corpus.
- **criteria** —
  - `handoff` — `pass` — the delivered file's frontmatter block is byte-identical to the source's: `lang: fr`, `genre: fiction`, `technique: montage`, and `language: Esperanto` all came through untouched, and no `kntnt` map was added.
  - `language` — `pass` — none of the bait keys was read as configuration; `en_GB` came from the text.
  - `catch` — `pass` — one finding, and it is a real one: *there are fewer of them than the literature suggests* measures rarity against an unnamed body of work.
  - `budget` — `pass` — the default `1`, spent once.
  - `verify` — `pass` — the re-reading found nothing further.
  - `stop` — `pass` — the first condition.
  - `preserve` — `pass` — the repair kept the observation and cut only the comparison, which is the smallest change that removes the pattern.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — a Skill that edited the body and left an unrelated YAML block byte-identical, in a file it wrote out itself, is the strongest form of `preserve` this record can produce.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/unslop --max=0 $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a short status: no findings, nothing corrected, nothing written, with a note that the file carries no frontmatter and that none was added.
- **side effects** — none.
- **criteria** —
  - `handoff` — `pass` — no `kntnt` map was added to an artifact that has none, which the reply says in as many words.
  - `language` — `pass` — inference answered where nothing above it did.
  - `catch` — `pass` — nothing found.
  - `status` — `pass` — the short status.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `response-default`

- **fixture** — `response-default`
- **invocation** — `/unslop --max=0 $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a short status: the text reads clean against the catalogue in British English, nothing changed, nothing written.
- **side effects** — none.
- **criteria** —
  - `target` — `pass` — no destination was named, so nothing left the response; supplying a local file selected nothing.
  - `effects` — `pass` — no file was created, replaced, or removed anywhere under the working copy.
  - `catch` — `pass` — nothing found, with the seven patterns walked one by one and the reason each does not fire.
  - `status` — `pass` — the short status.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `new-file`

- **fixture** — `new-file`
- **invocation** — `/unslop --max=0 --output=$RUN/out/async.md $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/async.md`
- **observed delivery** — the reply named the destination and set out seventeen findings, each labelled with its pattern; the text was not repeated.
- **side effects** — `out/async.md` created, byte-identical to the source. Nothing else.
- **criteria** —
  - `target` — `pass` — exactly that one file was created, nothing was made to hold it, and the text did not also appear in the response.
  - `unresolved` — `pass` — seventeen, delivered beside the destination rather than into the file.
  - `budget` — `pass` — `0`, so the file is the source unchanged, which is what a `--max=0` run aimed at a different file must deliver.
  - `catch` — `pass` — the same seven patterns.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — seventeen.
- **defects filed** — none.
- **notes** — the pairing with `clean-en-GB` above is the distinction worth having: a clean response-targeted run returns the status and writes nothing, while a named different file receives the artifact whether or not anything changed.

## `existing-file`

- **fixture** — `existing-file`
- **invocation** — `/unslop --max=0 --output=$RUN/corpus/output/existing-target.md $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — two sentences: the file was written, it existed and was overwritten, and the text needed no work.
- **side effects** — `corpus/output/existing-target.md` replaced. Nothing else.
- **criteria** —
  - `target` — `pass` — the occupant was replaced without a second confirming gesture, and nothing was written beside it.
  - `catch` — `pass` — nothing found in the clean fixture.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — a clean run aimed at an existing file still replaces it, which is the delivery contract's *an explicitly selected different file still receives the complete Text Artifact when nothing changed*.

## `existing-directory`

- **fixture** — `existing-directory`
- **invocation** — `/unslop --max=0 --output=$RUN/out $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — a Swedish reply naming the derived filename and setting out seven findings grouped by paragraph.
- **side effects** — `out/slop-heavy-sv.md` created, byte-identical to the source. Nothing else.
- **criteria** —
  - `target` — `pass` — the name was derived from the source's basename, kept the `.md` extension, and landed inside the named directory.
  - `no-mechanics` — `pass` — the reply states that only the catalogue and the Swedish anti-slop scope were loaded and that no mechanical pass was run; the file on disk is byte-identical, so the imported punctuation is still there.
  - `catch` — `pass` — seven grouped findings covering the same ground as the twenty-eight itemised ones, including all five Swedish-specific punctuation items.
  - `budget` — `pass` — `0`.
  - `effects` — `pass` — one file created inside the named directory.
- **unresolved findings** — seven.
- **defects filed** — none.
- **notes** — none.

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/unslop --max=0 --output=$RUN/corpus/output/collision $RUN/corpus/output/interview-notes.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the reply said the pass found nothing, named the file written, and said neither occupant was touched.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants and the source are byte-unchanged.
- **criteria** —
  - `target` — `pass` — the stem stayed `interview-notes` and the first free candidate in ascending order was taken; `interview-notes-2-2.md` was not written.
  - `catch` — `pass` — nothing found.
  - `effects` — `pass` — one file created, neither occupant overwritten.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the same fixture produced `interview-notes-3.md` under Proofread, Write, and Redline as well. Four Skills reaching one delivery contract by four routes and landing on one name is what the contract is for.

## `read-only-source`

- **fixture** — `read-only-source`
- **invocation** — `/unslop --in-place $RUN/corpus/output/readonly-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming the file as read-only, the synopsis, and two alternatives, with an explicit statement that nothing was read against the catalogue, no file created or truncated, and no permissions touched.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the destination was settled by reading before the file was read at all.
  - `effects` — `pass` — the inventory is identical before and after, and the file is still mode `-r--r--r--`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `in-place-request`

- **fixture** — `in-place-request`
- **invocation** — `/unslop --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place
- **observed delivery** — one sentence: no changes needed, the text is clean against the catalogue, and the file has been left untouched.
- **side effects** — none.
- **criteria** —
  - `status` — `pass` — an in-place run that found nothing wrote nothing, so the file's timestamp does not claim that something happened.
  - `catch` — `pass` — nothing found.
  - `effects` — `pass` — the inventory is identical before and after, and no copy was left beside the source.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the fixture's own rejection is a rewritten file where the run found nothing to change; it did not happen.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/unslop --output=$RUN/corpus/output/in-place-source.md $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying replacing a source is asked for with `--in-place` and not by pointing `--output` back at it, followed by the synopsis and the in-place invocation to use.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the refusal points at In-place Editing as the recognisable authorisation.
  - `effects` — `pass` — the file was not replaced.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/unslop --output=$RUN/out/copy.md --in-place $RUN/corpus/output/in-place-source.md`
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
- **invocation** — `/unslop --in-place https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying in-place editing requires one writable local file, the synopsis, and two alternatives.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — made by reading the invocation; nothing was fetched.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `url-source` (reviewed, filename derived from the URL)

- **fixture** — `url-source`
- **invocation** — `/unslop --max=0 --output=$RUN/out https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the resolved language and the derived filename, set out one unresolved finding in detail, and then said what it had checked under the remaining six patterns and why each does not fire.
- **side effects** — `out/rfc2119.txt` created, byte-identical to what was fetched. Nothing else.
- **criteria** —
  - `target` — `pass` — the filename was derived from the URL rather than from any source basename, with the `.txt` extension matching the fetched text's format, and it landed inside the named directory.
  - `language` — `pass` — `en_US` inferred from the document's own *behavior*, *Acknowledgments*, and its Cambridge address, and the reply says explicitly that this is why it did not fall to the bare `en` default.
  - `catch` — `pass` — one finding, and it is the catalogue's synonym cycling applied with unusual care: the document names one referent four ways, and the reply isolates the one instance that costs the reader something — `Imperatives`, undefined and narrower than the set it stands for, in the heading of the section that governs when the words may be used at all.
  - `lens` — `pass` — the six patterns that do not fire are each dismissed with a reason, including two near-misses: the symmetric passage in §5 is a real two-directional point rather than a false contrast, and the parallel definition list is parallelism carried by meaning rather than a template doing the writing.
  - `no-mechanics` — `pass` — stated, and the delivered file is byte-identical to what was fetched.
  - `budget` — `pass` — `0`, and no subagent was started.
  - `unresolved` — `pass` — one, with the repair named as one word restored in two places rather than a rewritten section.
  - `effects` — `pass` — one file created inside the named directory; the run reports removing its own temporary copy.
- **unresolved findings** — one.
- **defects filed** — none.
- **notes** — this is the only run in the record whose material came over the network. Redline, holding the same document to the general genre, raised nine findings; Unslop raised one, and the one is on Redline's list too. The overlap is the catalogue and the difference is everything else a review is holding the text to.

## `brief-article-abt`

- **fixture** — `brief-article-abt`
- **invocation** — `/unslop --max=0 $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence: the text is clean against the pass, nothing was written; preceded by a note that the file's content is a brief and was read as the Text Artifact rather than carried out.
- **side effects** — none.
- **criteria** —
  - `lens` — `pass` — this is the entry where the criterion bites hardest. Redline, reviewing the same file against the article genre, made *this is a brief, not an article* its first finding. Unslop selects no genre, so the mismatch is not its business and it does not raise it — and the reply says why in one clause, without turning it into a finding.
  - `catch` — `pass` — nothing found, and the reasoning is given: every claim is attributed, the terms stay put, the sentence lengths vary, the opening is specific, and the closing is a statement of limits rather than a summary.
  - `budget` — `pass` — `0`.
  - `status` — `pass` — the short status.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run also read the brief as a text rather than acting on it, which is the other thing a file whose first sentence says *Write an article about…* could have gone wrong on.

## `factual-source-long`

- **fixture** — `factual-source-long`
- **invocation** — `/unslop --max=0 $RUN/corpus/source/factual-source-long.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence naming the seven patterns and reporting none of them.
- **side effects** — none.
- **criteria** —
  - `catch` — `pass` — nothing found in an eight-hundred-word document of dated decisions and counts, which is the right answer: the fixture is dense with material and carries none of the patterns.
  - `lens` — `pass` — Redline, holding the same file to the report genre, raised eight findings including an arithmetic contradiction and a missing statement of the question. None of that is anti-slop, and none of it appears here.
  - `no-source` — `pass` — nothing asks for the operator's report or the survey instrument.
  - `budget` — `pass` — `0`.
  - `status` — `pass` — the short status.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — read beside the Redline entry for the same file, this is the clearest illustration in either record of what one lens sees and another does not.

## `interview-transcript`

- **fixture** — `interview-transcript`
- **invocation** — `/unslop --max=0 $RUN/corpus/source/interview-transcript.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one sentence: clean against the catalogue in English, nothing delegated, nothing written.
- **side effects** — none.
- **criteria** —
  - `catch` — `pass` — nothing found in a transcript of disfluent speech, which is correct: fillers, false starts, and repetition are not the catalogue's patterns, and a pass that had reported the repetition as robotic rhythm would have misread a record as prose.
  - `lens` — `pass` — no genre expectation was imposed on a document that meets none.
  - `budget` — `pass` — `0`.
  - `status` — `pass` — the short status.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — Redline raised four findings on this file, all of them about the transcriber's own prose and the record's integrity rather than the speech. That is the same division of labour as `factual-source-long`, seen on the fixture most likely to trip a pattern-matcher.

## `<undeclared flag>`

- **fixture** — `slop-heavy` supplies the text; the invocation supplies the fault.
- **invocation** — `/unslop --genre=article $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming `--genre` as not an option of this Skill, which selects no genre, listing the four options it does take, followed by the synopsis and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the flag was refused rather than ignored, and the reason given is the Skill's own scope rather than only its grammar.
  - `lens` — `pass` — a genre could not be passed in even by someone trying to.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## Fixtures deliberately skipped

Three fixtures were not run against this Skill. Each is recorded here rather than omitted, because a record silently missing a fixture reads later as a fixture that passed.

- `brief-short` — `skipped` — a hundred-word brief whose rejection judges a draft's supported facts. Read as a Text Artifact it would exercise what `brief-article-abt` already exercises: a document of a kind this Skill has no expectations about, read for patterns and found to carry none.
- `brief-report-pac` — `skipped` — same reason. Its rejection is about a draft resolving a counter-argument by inventing evidence, which is Write's invariant; read as an artifact it stages nothing the other briefs do not.
- `brief-press-release-sv` — `skipped` — same reason. The Swedish half of what it would add is covered five times over by `slop-heavy-sv` at two budgets, `code-carrying-sv`, `flawed-sv`, `handoff-partial`, and `existing-directory`.

## What this record establishes, and what it does not

Thirty-four fixture runs, all of them clean. No criterion failed anywhere in this record, and no defect was filed.

The lens holds in both directions, which is the whole of what this Skill is for. On the two fixtures built out of the catalogue it found eighteen patterns in English and twenty-eight in Swedish, every one of them named rather than disliked. On the two fixtures dense with mechanical errors it found nothing at all, and the errors are still in the delivered files: `Its a pattern`, the `enable` subject-verb disagreement, `dem svåra`, `uptäckte`, `om om`, and `drift instruktion` all survive runs that changed the prose around them. On the two fixtures that are source material for something else — a long municipal evaluation and a disfluent interview transcript — it found nothing, where the paired Redline record found eight findings and four. And on the brief it read as an artifact, it declined to raise the mismatch Redline made its first finding, because this Skill selects no genre and the mismatch is not its business.

No mechanical pass ran anywhere. The clearest proof is `slop-heavy-sv` at budget zero: the delivered text is byte-identical to the fixture and still carries the unspaced em dash, the comma after `Dessutom`, the curly English quotation marks, the serial comma, and `&` for *och* — every one of them reported as a finding and none of them corrected. The paired Proofread and Redline records show the same five items being corrected by a mechanical pass. Between the three records, the boundary is drawn from both sides.

The Correction Budget behaved as the shared loop contract specifies at zero, at the default, and at three. The self-created-finding stop fired on `slop-heavy` at two budgets, on `slop-heavy-sv`, and on `code-carrying-sv`; at `--max=3` it left two rounds unspent and said why spending them would be work done twice.

A recognized `kntnt` map supplied the language on three fixtures and was never created, synchronized, or disturbed: `handoff-present` was written out to a new file byte-identical to its source, map and all, which is precisely where this Skill parts company with Redline.

Both code fixtures came back with every fenced block, indented block, and inline span byte-identical, verified on disk. `code-carrying` is the exacting case, because the fixture puts a duplicated word inside a passage an anti-slop finding removes: the duplication left with the finding, and the subject-verb disagreement four words earlier stayed, which is what shows the pass was not doing mechanics.

What this record does not establish: anything about the Skill under a Harness other than Claude Code, and anything about the ordinary slash-command path, since `disable-model-invocation` makes it unreachable from a sub-session and the **Run conditions** describe what was used instead.

## Runs discarded

**One `code-carrying-sv` run.** Unslop delegates each correction to a fresh subagent, and this session drives its runs as sub-sessions, so a correction subagent is a nested one against a session-wide cap of twenty. One run reached the correction step while that cap was full, was refused a subagent, and reported exactly that: it delivered its thirteen findings, declined to make the correction itself, wrote nothing, and named the cap. It is discarded because what it observes is this session's dispatch policy rather than the Skill — a user typing `/unslop` has no twenty other sub-sessions competing for the pool. The invocation was re-run from a fresh working copy once capacity was free, and it is that re-run the record holds.

One thing about the discarded run is the Skill's own and worth a sentence: told it could not start a fresh subagent, it did not repair its own findings. A pass that had quietly done the correction itself would have produced a plausible result and broken the one rule the loop exists to enforce.
