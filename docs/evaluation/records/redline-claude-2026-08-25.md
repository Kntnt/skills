# redline — claude — 2026-08-25

- **record** — `redline-claude-2026-08-25`
- **date** — `2026-08-25`
- **ticket** — `#109`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.245
- **corpus commit** — `6d476db`

## Run conditions

The Skill was run as a user of it runs it: `/redline …` as the whole of a Claude Code turn, against the Skill as installed at `~/.agents/skills/redline`, reached through `~/.claude/skills/redline`, which symlinks to it. The installed Skill was byte-identical to `skills/editorial/redline/` at the corpus commit, the Proofread Skill it depends on was byte-identical to `skills/editorial/proofread/`, and the Collection Library both resolve through was byte-identical to `skills/kntnt/`. None of that was assumed: `diff -r` was run against all three before the first run and reported no difference.

The install did not begin that way. Redline was not installed on this machine at all, and the Library that was installed predated the genres, the techniques, the anti-slop catalogue, and the base review extension — so `--genre=article`, `--technique=abt`, and the whole of the review half named resources that were not there. The Skill was therefore installed and the Library brought up to the corpus commit, with the previous Library kept aside and put back when the runs were finished, and the installed Redline removed again; the machine ends as it began.

Forty-three invocations are recorded below, and four more under **Runs discarded**; two further entries carry no invocation of their own — `response-default`, which is a situation every destination-less run exercises, and `interview-transcript`, which was not run and says why. Thirty-six of the forty-three were made first; the last seven, under **Criteria the corpus could not stage on its own**, were made afterwards, one at a time with nothing else in flight, to judge three criteria the corpus supplies no material for. They ran under the same install, the same harness, and the same before-and-after inventory, and four of them staged run-local probe material as `$RUN/probe/` beside `$RUN/corpus/`, quoted in full where they are recorded. Each ran in its own turn with no memory of any other, and in its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says: `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/109.scratch/runs/<id>`; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form. **side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself.

The runs were driven from the user's home directory rather than from this repository, so no run read this repository, the ticket, the criteria below, or the Skill's own source. Each run did inherit `~/.claude/CLAUDE.md`, which every session on this machine inherits; it is recorded because two of its instructions are visible in the traces — runs cleaned up their own temporary files and checked for stray background shells before finishing — and neither touches editorial behaviour.

Judging was done from the delivered reply, the filesystem inventory, and the run's own recorded tool trace, fixture by fixture, before any GPT-family record existed to compare with. The tool trace is part of the evidence because three of this Skill's obligations are invisible in the reply by design: what a correction subagent was actually given, whether a returned correction was reviewed again, and whether the mechanical pass ran once. The Skill's contract keeps that correspondence out of its output, so a record judging it from the output alone could only take the run's word for it. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

`/redline` is unambiguous on this machine even though a legacy plugin, `kntnt-text-skills:redline`, is installed beside the Collection's Skill and answers to a similar name. Every run below reached the Skill under evaluation with no routing hint, which is visible in each run's own trace: each starts by running the Collection's checker and reading the Collection's `help.md`.

The criterion identifiers are stable across entries:

- `precedence` — each of genre, technique, and language settled at the level the resolution order gives it, and independently of the others.
- `language` — the resolved language reaches the review and the mechanical pass, and the run answers in it where the artifact is in it. Recorded separately from `precedence` where a language is the point of the entry rather than one parameter among three.
- `review` — the initial review produces findings the artifact warrants, naming where, which requirement, and what the reader loses.
- `anti-slop` — the catalogue's patterns are found by name rather than as style preference, in the resolved language.
- `budget` — the Correction Budget bounds the loop: `0` corrects nothing, a positive value is a ceiling and never a quota.
- `fresh` — every correction is delegated to a subagent started fresh, receiving the complete current text and the complete current findings.
- `verify` — every correction is followed by a fresh review rather than accepted on the corrector's report.
- `stop` — the loop stops where the contract says it stops, and says which of the three conditions stopped it.
- `no-source` — the artifact is never compared with source material and the absence of it is never remarked on.
- `mechanics` — Proofread is invoked exactly once, after all review and correction, and nothing substantive follows it.
- `findings` — findings left over are delivered with the artifact and routed as the contract routes them.
- `sync` — a recognized `kntnt` map is synchronized to the resolved configuration, no map is added where none existed, and nothing else in the frontmatter changes.
- `loading` — only what step 5 names is read.
- `ask` — a materially mixed language produces a question rather than a guess.
- `target` — the artifact went where the output contract sends it.
- `effects` — the filesystem shows what the contract allows and nothing else.
- `refusal` — a refused invocation names the problem, prints the synopsis, points at help, and leaves nothing behind.
- `leak` — the review's own working, and its correspondence with a subagent or a nested Skill, stay out of the output.

Two things about the criteria are worth a later reader's attention.

`anti-slop` is judged in English on every corpus fixture, and every Swedish corpus entry below records it as `skipped`. The corpus carries one fixture of concentrated slop and it is English; its Swedish fixtures are competent prose whose defects are mechanical or structural, and a Skill that finds no pattern in a text that has none has not been tested for whether it would find one. The Swedish half is judged instead on run-local material, under **Criteria the corpus could not stage on its own** below, where all seven of the catalogue's patterns are found in Swedish on Swedish instances. The gap is in the corpus rather than in the Skill, and #142 is where it is written down and stays open.

`precedence` in the form the ticket names — a flag, a metadata value, and a contextual value each settling a different parameter in one invocation — cannot be staged from this corpus. Both fixtures carrying a `kntnt` map carry a complete one, so the map always outranks any Contextual Instruction for all three parameters at once and a contextual value can never settle anything beside it. What the corpus entries below establish is the same independence in the arrangements the corpus does reach: `handoff-conflicting` settles two parameters by flag and takes the third from the map, `handoff-unusable` shows one flag deciding whether the same unusable map stops a run, and `frontmatter-unrelated` settles one by flag, one by Contextual Instruction, and one by inference. The three-source form is judged on run-local material carrying a one-key map, under **Criteria the corpus could not stage on its own** below, in two invocations that rotate which source settles which parameter. The missing partial-map fixture is #142's second half and stays open.

`stop` names which of the three conditions ended a loop, and the corpus reaches two of them on its own: no findings with the budget unspent, and the budget spent with findings left. The third — a correction that makes no relevant progress — needs a review whose remaining findings a corrector may not repair, and no corpus fixture run at the genre it was written in produces one. It is judged below on two corpus fixtures held to a genre they are not written in, which needs no new material and no change to the corpus: only the invocation is new.

## `slop-heavy` (review only, budget zero)

- **fixture** — `slop-heavy`
- **invocation** — `/redline --max=0 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back unchanged in the response, followed by ten numbered findings, each naming where in the text, which requirement, and what the reader loses, and each marked unresolved; nothing was written.
- **side effects** — none. The inventory is identical before and after.
- **criteria** —
  - `review` — `pass` — ten findings on a text the corpus supplies as concentrated slop, each located in a named paragraph.
  - `anti-slop` — `pass` — the patterns are named rather than disliked: the empty opening, four false contrasts quoted individually, importance inflation with its instances, vague attribution across five claims, generic conclusion, robotic rhythm as three anaphoric triplets in three consecutive paragraphs.
  - `budget` — `pass` — `0` delegated nothing; findings 2, 3, and 9 are marked as not repairable from the artifact, which is a statement about the findings rather than an attempt at them.
  - `no-source` — `pass` — no remark anywhere that the material behind the essay was unavailable; the findings that need it say the *artifact* does not carry it, which is a judgement about the text.
  - `mechanics` — `pass` — `proofread/SKILL.md` read once and the `mechanics` scope resolved once, after the review; the pass found nothing and nothing followed it.
  - `findings` — `pass` — all ten delivered with the artifact and marked unresolved.
  - `sync` — `pass` — the artifact carries no `kntnt` map and none was added.
  - `loading` — `fail` — an incorrect side effect of the reading kind rather than the filesystem kind: `general` was resolved, and `genres/article.md` and `genres/article.review.md` were read beside `genres/general.md`.
  - `target` — `pass` — no destination named, the response received the artifact.
  - `effects` — `pass` — the inventory is identical before and after.
  - `leak` — `pass` — no correspondence, no reasoning about passages dismissed, no account of the mechanical pass beyond the one line saying it ran.
- **unresolved findings** — ten, all of them.
- **defects filed** — #140.
- **notes** — the corpus's floor holds: the review does not find nothing, and no finding is phrased as style preference where the pattern has a name.

## `slop-heavy` (default budget)

- **fixture** — `slop-heavy`
- **invocation** — `/redline $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a corrected text of two short paragraphs came back in the response, followed by a list of what the correction resolved and five findings left standing, two of them newly found by the re-review.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — the same patterns found as in the run above, on a genre resolved by inference to `article` rather than `general`.
  - `anti-slop` — `pass` — the resolved list names vague attribution, the empty opening, the generic closing, four false contrasts, three anaphoric triples, importance inflation, and two decorative connectives.
  - `budget` — `pass` — the default of `1` was spent once and no more; the run says so and the trace shows one delegation.
  - `fresh` — `pass` — one subagent, started fresh, whose whole instruction was a brief carrying the complete current text and the complete findings verbatim.
  - `verify` — `pass` — the re-review found two things the first review had not, and the run says which and admits it missed them; a report accepted on trust could not produce that.
  - `stop` — `pass` — the budget was spent with findings left, and those findings were carried forward and named as unresolved.
  - `no-source` — `pass` — the three unrepairable findings say the text needs material *it does not carry*, and nothing asks for it or notes its absence as a caveat on the review.
  - `mechanics` — `pass` — once, after the correction, and nothing substantive after it.
  - `findings` — `pass` — five delivered with the artifact, each marked unresolved or new.
  - `loading` — `pass` — `article` was resolved and `genres/article.md` and its review half were the only genre resources read.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing created, replaced, or removed.
  - `leak` — `pass` — the subagent's own account of its work does not appear.
- **unresolved findings** — five: no angle, asserts rather than reports, the title, terminology cycling, and a paragraph following from nothing.
- **defects filed** — none.
- **notes** — the correction cut roughly seven-eighths of the draft, and the corpus's floor for this fixture rejects *a correction that removes the patterns and the content with them*. This run stays on the right side of it: what went is the empty opening, the generic conclusion, the categorical claim about traditional meetings, and every claim attributed to nobody — cutting being the catalogue's own prescribed repair for the last two, since it forbids furnishing an unsourced claim with a source — and every claim the draft actually supported survives, the distributed-teams one included. The magnitude is recorded because a later reader comparing families will want it: 450 words in, 55 out. The `--max=3` entry above is the same behaviour past that line, and #144 is where the difference between them is written down.

## `slop-heavy` (budget of three)

- **fixture** — `slop-heavy`
- **invocation** — `/redline --max=3 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a resolved configuration saying all three rounds were spent, then a text of two sentences, then three unresolved findings and a paragraph listing what the rounds had repaired.
- **side effects** — none.
- **criteria** —
  - `budget` — `pass` — three rounds, three delegations, and the run's own narration counts them down as it goes: *Round 1 spent (2 remaining)*, *Round 2 spent (1 remaining)*, *Budget spent (3/3), findings remain*.
  - `fresh` — `pass` — three subagents, each started fresh, each given the text as it then stood and the findings of the review immediately before it. The briefs are on record and show the text they carried shrinking with the rounds: 333 words, then 84, then 63.
  - `verify` — `pass` — each round is followed by a re-review from the top, and the findings that reach the next round are that review's rather than the corrector's report.
  - `stop` — `pass` — stopped on the third of the three conditions, the budget spent with findings left, and carried them forward as unresolved.
  - `review` — `pass` — twelve findings on the original, and the reviews after each round were live enough to find what the round before had introduced.
  - `anti-slop` — `fail` — an incorrect side effect in the sense the corpus's floor names for this fixture: *a correction that removes the patterns and the content with them*. The delivered text is about fifty words from a draft of about four hundred and fifty, and it is shorter than the `--max=1` run's result on the same fixture by content rather than by patterns — the claim about distributed teams collaborating across time zones survives one round and not three. The run's own second finding is the sharper evidence: a later round cut *respecting focus* from the body as a repetition of the heading, and the review then reported that the title names a claim the body no longer makes. A repair created the finding.
  - `findings` — `pass` — three delivered, marked unresolved, with the one to settle first named.
  - `no-source` — `pass` — the first finding says restoring substance means *going back to material that would have to be reported, not invented*, and nothing asks for it.
  - `mechanics` — `pass` — once, after the loop, and it found nothing.
  - `loading` — `pass` — `article` resolved by inference, `genres/article.md` and its review half the only genre resources read.
  - `sync` — `pass` — no map, none added.
  - `target` — `pass` — response.
  - `effects` — `pass` — the file on disk is byte-identical to the corpus.
  - `leak` — `pass` — the three subagents' own accounts do not appear; what the rounds repaired is stated in the run's own voice.
- **unresolved findings** — three: no material and therefore no article, a title the body no longer supports, and an abstract prescription.
- **defects filed** — #144.
- **notes** — every round was locally correct, which is what makes this worth filing rather than dismissing: the repairs are the catalogue's own prescribed ones, each round made real progress on the findings it was given, and the loop's no-progress condition therefore never fired. What has no owner is the trend across rounds, which only the dispatching run can see and which nothing asks it to look at. Read beside the `--max=1` entry above, the pair is the finding: a longer budget reached a worse text on the same fixture. This fixture's first run at this budget is recorded under **Runs discarded**; this entry is the re-run made on its own.

## `slop-heavy` (findings routed beside a file)

- **fixture** — `slop-heavy`
- **invocation** — `/redline --max=0 --output=$RUN/out/slop.md $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/slop.md`
- **observed delivery** — one line naming the file that received the artifact and saying it was unchanged, the resolved configuration, and ten unresolved findings in the response beside it; the text itself was not repeated.
- **side effects** — `out/slop.md` created. Nothing else; the source is byte-identical to the corpus.
- **criteria** —
  - `findings` — `pass` — this is the routing the contract asks for: the artifact to the file, the findings to the response beside it, and the file still created although nothing in the text changed, because creating it was what the invocation requested.
  - `review` — `pass` — ten findings, located and named.
  - `anti-slop` — `pass` — the seven patterns are all named, with instances quoted.
  - `budget` — `pass` — `0`, nothing delegated.
  - `no-source` — `pass` — the closing note says the text needs source material and does not remark that the review lacked it.
  - `mechanics` — `pass` — once, and it changed nothing.
  - `loading` — `pass` — `general` resolved, `genres/general.md` the only genre read.
  - `target` — `pass` — exactly the named path was created and it holds the artifact.
  - `effects` — `pass` — one file created, and it is the one named.
  - `leak` — `pass`.
- **unresolved findings** — ten, delivered in the response.
- **defects filed** — none.
- **notes** — this and the two entries above resolved the same fixture's genre three ways — `general` twice and `article` once, all by inference with nothing named. The genre reached is a judgement about the text and the corpus asserts nothing about which is right; it is recorded because a later reader comparing families should not read a difference of genre as a difference of behaviour.

## `clean-en-GB`

- **fixture** — `clean-en-GB`
- **invocation** — `/redline $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line saying what it was reviewed against, a two-word no-change verdict, and one line of resolved configuration recording the budget as unspent. The text was not repeated.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — a review that finds nothing on competent prose is the correct outcome for this fixture, and the run says what it was read against rather than merely asserting it was clean.
  - `budget` — `pass` — the default `1` went unspent, which is the contract's *up to it and never towards it*.
  - `stop` — `pass` — stopped on the first of the three conditions, no findings, with the budget unspent, and said so.
  - `mechanics` — `pass` — once, and it changed nothing; the fixture's tempting British forms — `judgement`, `summarise`, `towards`, `fortnight`, and the absent serial comma — all survived.
  - `findings` — `pass` — none to deliver, and none invented.
  - `loading` — `pass` — `general` resolved and read, no second genre, no technique.
  - `target` — `pass` — a clean response-targeted run that changed nothing wrote nothing and returned the short status, which is what the contract asks for instead of repeating the text.
  - `effects` — `pass` — nothing touched.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the fixture that tests the temptation to rewrite competent prose, and the run declined it without being asked to.

## `flawed-en-US` (default budget, response)

- **fixture** — `flawed-en-US`
- **invocation** — `/redline $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line saying two substantive defects were found, repaired, and verified by re-review, then the complete corrected text; nothing was written.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — two findings, each located in a named paragraph: a generalisation from one case (*five other things … each of them was load-bearing*, evidenced once) and a throat-clearing opener the paragraph does not need.
  - `budget` — `pass` — the default `1`, spent once.
  - `fresh` — `pass` — the brief the subagent received is on record: it opens *You have not seen this text before, and there is nothing you are expected to remember*, carries the complete text as it then stood and both findings as the review wrote them, names the resolved genre, technique, and language, and requires everything the findings do not concern to come back unchanged.
  - `verify` — `pass` — the returned text was reviewed again before the mechanical pass, and the run's narration marks the re-review as a separate step.
  - `stop` — `pass` — stopped clean after one round with nothing left.
  - `no-source` — `pass` — nothing asks for the importer, the tickets, or any material behind the text.
  - `mechanics` — `pass` — after the correction, once, and the American forms `normalize` and `catalog` survived it.
  - `loading` — `pass` — `general` only.
  - `target` — `pass` — response, and the source file is byte-identical to the corpus.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor for this fixture is written for a mechanics-only pass — *American spellings changed to British ones, sentences restructured, hedges added or removed, or the closing opinion softened* — and Redline's contract puts substantive correction inside its own scope, so the floor and the contract meet here. Judged against the contract: the spellings survived, the closing opinion survived, and the two changes are the two the review named. The deleted sentence, *The decision to rewrite it wasn't taken lightly*, is a hedge by the corpus's reading and throat-clearing by the review's. It is recorded rather than resolved, because a corpus that only ever meets a mechanical pass would have said less about this fixture than it does.

## `flawed-sv`

- **fixture** — `flawed-sv`
- **invocation** — `/redline $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line saying the editorial review found nothing, that the budget therefore went unspent, and that only the closing mechanical pass changed anything, then the complete corrected Swedish text; nothing was written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `sv` inferred from the text with no flag, no map, and no instruction in play, and the mechanical pass corrected Swedish mechanics rather than translating anything.
  - `mechanics` — `pass` — once, at the end: `det det` → `det`, `dem svåra` → `de svåra`, `uptäckte` → `upptäckte`, `avgångs samtal` → `avgångssamtal`, `Antalet ärende` → `Antalet ärenden`, and the missing word restored in *tänker inte tillbaka* → *tänker inte gå tillbaka*. The informal `hen` was left alone, which the corpus asks for and which a pass reaching for a rule would have changed.
  - `review` — `pass` — the review found no substantive defect in four paragraphs of competent Swedish, and said what it had judged rather than only that it had found nothing.
  - `budget` — `pass` — the default `1` went unspent.
  - `stop` — `pass` — stopped on no findings with the budget unspent.
  - `anti-slop` — `skipped` — the Swedish anti-slop scope was loaded and applied to a Swedish text that carries none of its patterns, so this run cannot say whether they would be caught; see #142.
  - `no-source` — `pass` — nothing asks for the case data behind the argument.
  - `findings` — `pass` — none to deliver, and none invented.
  - `loading` — `pass` — `general` only.
  - `target` — `pass` — response; the file on disk is byte-identical to the corpus.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor holds on all three counts: the answer is Swedish, the argument is unchanged, and `hen` survives. The delivered text is the fixture with six mechanical repairs and nothing else, which is a mechanical pass reaching a language whose mechanics differ from English rather than a review that found the text acceptable and stopped looking. This fixture's first run is recorded under **Runs discarded**; this entry is the re-run made on its own.

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/redline $RUN/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a first line stating that the And/But/Therefore shape is not grounds to hold the text to ABT and that it was not, then the corrected text; the source was named as untouched.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — no technique resolved, and the run says why in the terms the contract uses. Genre `general`, language `en_GB` by inference.
  - `review` — `pass` — one finding, repaired: the title named the wrong noun for the thing the piece is about.
  - `budget` — `pass` — one, spent once.
  - `fresh` — `pass`.
  - `verify` — `pass`.
  - `stop` — `pass` — clean after one round.
  - `loading` — `pass` — `general` only, and no technique resource was read at all, which is the load-side half of the same rule.
  - `mechanics` — `pass` — once, found nothing.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus rejects a resolved technique of ABT *reported, recorded in metadata, or acted on*. None of the three happened: no technique was reported, no map was added to a file that has none, and the paragraph opening on *Therefore* — the fixture's most direct bait — was left exactly as it was.

## `mixed-language`

- **fixture** — `mixed-language`
- **invocation** — `/redline $RUN/corpus/prose/mixed-language.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a question. The run quoted a sentence that switches language mid-clause, said neither language is dominant, offered `sv`, `en_GB`, and `en_US` with what each would make of the other language's stretches, offered the reading in which the mixing is deliberate, and stopped.
- **side effects** — none.
- **criteria** —
  - `ask` — `pass` — named the candidates and asked before anything was reviewed, which is what the contract asks for and what the corpus's floor requires instead of a silent pick.
  - `precedence` — `pass` — genre and technique were settled — `general`, none — and reported as settled, while only the language was held open. That is per-parameter resolution doing its job on the one parameter that could not be settled.
  - `effects` — `pass` — nothing written, which the run states as the reason the question costs nothing to answer either way.
  - `review` — `skipped` — nothing was reviewed, which is the correct outcome for this fixture.
  - `mechanics` — `skipped` — the run stopped before it.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the question is a real question rather than a refusal dressed as one: it names what it would do under each answer, which is what makes it answerable in one word.

## `locale-divergent` (British English)

- **fixture** — `locale-divergent`
- **invocation** — `/redline --language=en_GB --max=0 $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text back byte-identical, with a line saying the mechanical pass found no errors, then three unresolved findings.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — `en_GB` from the flag; genre `general` inferred; no technique.
  - `mechanics` — `pass` — nothing changed. `organised`, `licence` as a noun, the pound figure, and the full stop outside the closing quotation mark are all British forms and all survived, which is the half of this fixture the corpus most cares about.
  - `review` — `pass` — three findings, the first of them the numeric date.
  - `budget` — `pass` — `0`.
  - `findings` — `pass` — all three delivered and marked unresolved.
  - `no-source` — `pass`.
  - `loading` — `pass` — `general` only.
  - `target` — `pass` — response, nothing written.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — three: the unreadable `3/4`, a recommendation covering two tools on a case that reaches one, and a restating first sentence in the last paragraph.
- **defects filed** — none.
- **notes** — the corpus rejects the ambiguous date being rewritten on the assumption of a locale, and the run makes exactly that argument in the finding: it lists the British evidence, says it points at 3 April, and then says a two-part numeric date is the one place that evidence stops being decisive. It asks rather than rewrites.

## `locale-divergent` (American English)

- **fixture** — `locale-divergent`
- **invocation** — `/redline --language=en_US --max=0 $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text with its mechanics moved to American conventions, and four unresolved findings, the second of which is that the document's own locale contradicts the one the invocation resolved.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — `en_US` from the flag, against a text whose own conventions are British throughout; the flag won, which is what level 1 is for.
  - `mechanics` — `pass` — `organised` → `organized`, `judgement` → `judgment`, `cancelling` → `canceling`, `specialised` → `specialized`, `licence` → `license`, and the full stop moved inside the closing quotation mark. Under a resolved `en_US` these are not valid alternatives but errors, and the corpus's floor rejects British forms treated as errors only *where British English is the resolved locale*.
  - `review` — `pass` — four findings, and the second is the one that matters here: it says which changes were made, that they are right if `en_US` is right and wrong if the document is genuinely British, and what to do either way.
  - `budget` — `pass` — `0`.
  - `findings` — `pass`.
  - `target` — `pass` — response, nothing written.
  - `effects` — `pass` — the file on disk is byte-identical to the corpus; the locale change exists only in the delivered text.
  - `loading` — `pass` — `general` only.
  - `leak` — `pass`.
- **unresolved findings** — four, including the locale contradiction and, again, the unrewritten `3/4`.
- **defects filed** — none.
- **notes** — `autumn` and `has got harder` were left alone and named as vocabulary rather than mechanics, which is the boundary the mechanical pass is contracted to keep. Read beside the British run, the pair is the clearest evidence in this record that the resolved locale reaches the mechanics: the same file, two locales, two different sets of changes, and the same refusal to touch the date.

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/redline --max=0 $RUN/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a first line naming what the review was read against, then the complete artifact with its frontmatter intact, then three unresolved findings.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — all three parameters fell through to the map and were reported in its own normalized spellings: `article`, `abt`, `en_GB`. Nothing was named on the invocation and nothing lower was consulted.
  - `sync` — `pass` — the map already said what the run resolved, so synchronising it changed nothing, and nothing else in the frontmatter changed either. The artifact comes back byte-identical.
  - `review` — `pass` — three findings, each against a named requirement of the genre, the technique, or the base contract.
  - `anti-slop` — `pass` — the second finding is a false contrast, named as one and quoted: *the question … is not whether the archive is worth keeping, which nobody disputes*.
  - `budget` — `pass` — `0`.
  - `findings` — `pass`.
  - `no-source` — `pass` — the first finding is an internal contradiction, which the contract keeps as an ordinary finding, and nothing asks for the archive's figures.
  - `mechanics` — `pass` — once, found nothing.
  - `loading` — `pass` — `article`, `article.review`, `abt`, `abt.review`, and no other genre or technique.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — three.
- **defects filed** — none.
- **notes** — the corpus rejects the map being ignored and its values reported in another spelling. Neither happened.

## `handoff-present` (an inert Contextual Instruction)

- **fixture** — `handoff-present`
- **invocation** — `/redline --genre=report --max=0 $RUN/corpus/frontmatter/handoff-present.md -- Review it as a PAC piece in Swedish.`
- **contextual instruction** — `Review it as a PAC piece in Swedish.`
- **output target** — `response`
- **observed delivery** — no review. The run set out the precedence correctly — the flag settles the genre at level 1, the map settles the technique and the language at level 2 and suppresses the instruction for both — and then stopped on that, under the heading *Context refusal*, saying that guidance wholly ineffective against a higher-precedence source is refused rather than silently dropped. It listed what nothing had done, and gave the invocation that would work.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — the reasoning is exactly right, parameter by parameter, and it says which of the three the flag legitimately overrides and which two the map settles.
  - `refusal` — `fail` — an unresolved mandatory finding, in the sense the protocol names: the invocation is valid, the artifact was supplied, and neither findings nor an artifact came back. `## Arguments` lists the invalid forms and this is not among them, and `## Resolution` already says what happens to a value a higher level has settled against — it is suppressed for that parameter, which is what the levels are for.
  - `review` — `fail` — nothing was reviewed.
  - `mechanics` — `fail` — the closing pass never ran, on a run that was not refused by any listed form.
  - `effects` — `pass` — nothing was written, which the run states.
  - `leak` — `pass` — vacuously.
- **unresolved findings** — none delivered, which is the failure.
- **defects filed** — #141.
- **notes** — the reason given is the one the contract writes about **flags**: *a flag accepted and ignored teaches that flags sometimes do nothing*. A flag is settled by the invocation's own grammar; a Contextual Instruction sits at level 3 of a precedence the artifact itself participates in, and being outranked there is the ordinary case rather than an error. Read beside the `frontmatter-unrelated` entry, where a Contextual Instruction settled the technique because no map was there to outrank it, the pair shows the mechanism working and then stopping a run for working.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/redline --language=sv --genre=article --max=0 $RUN/corpus/frontmatter/handoff-conflicting.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line stating the resolution parameter by parameter, then the artifact with its map rewritten, then three findings in Swedish.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — this is per-field resolution shown in one invocation: the flags settle the genre and the language against a map that says otherwise, the invocation names no technique, and `pac` is taken from the map. The run states each of the three and where it came from.
  - `sync` — `pass` — the map comes back as `genre: article`, `technique: pac`, `language: sv`, which is what the run resolved and not what the file said. Nothing else in the frontmatter changed, and the body is unchanged.
  - `language` — `pass` — the findings are written in Swedish, and the mechanical pass reports on Swedish mechanics: särskrivning, V2 order, double definiteness in *den gamla kön*.
  - `review` — `pass` — three findings, two against the PAC technique taken from the map and one against the base contract.
  - `budget` — `pass` — `0`, and the findings say so.
  - `anti-slop` — `skipped` — Swedish text carrying none of the patterns; see #142.
  - `findings` — `pass`.
  - `no-source` — `pass`.
  - `mechanics` — `pass` — once, found nothing.
  - `loading` — `pass` — `article`, `article.review`, `pac`, `pac.review`; the map's `report` was not read.
  - `target` — `pass`.
  - `effects` — `pass` — the file on disk is byte-identical; the synchronised map exists only in the delivered artifact, which is where a response-targeted run's result belongs.
  - `leak` — `pass`.
- **unresolved findings** — three.
- **defects filed** — none.
- **notes** — the corpus rejects a metadata value overriding an explicit one, an explicit value for one parameter suppressing the map for the others, and the file delivered with a map still contradicting what the run resolved. None of the three happened.

## `handoff-unusable` (nothing suppresses the map)

- **fixture** — `handoff-unusable`
- **invocation** — `/redline $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a stop before the review. The run named the value, named the file, listed the installed Language Resources, said the invocation carried no `--language=` so nothing settled that parameter ahead of the map, and stated that a near-miss spelling never becomes `en_GB` on its own. It then offered the two ways forward.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — the map was consulted at level 2 because level 1 was silent, and the unusable value at that level stopped the run rather than falling through to level 3.
  - `refusal` — `pass` — reported as unusable artifact metadata, which is the diagnostic the contract names for this case rather than the syntax refusal, and it names the problem and what would fix it.
  - `effects` — `pass` — nothing reviewed, corrected, or written; the inventory is identical.
  - `review` — `skipped` — the run stopped before it, correctly.
  - `mechanics` — `skipped` — likewise.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus rejects `en_UK` quietly read as `en_GB` and the run continuing as though the metadata had been usable. It also notes, correctly, that `genre: article` and `technique: abt` both resolve and that the language alone stops the run — which is per-parameter validation reported as such.

## `handoff-unusable` (a flag supersedes the map)

- **fixture** — `handoff-unusable`
- **invocation** — `/redline --language=en_GB --max=0 $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the review ran. The reply says the map's `en_UK` did not stop the run because the invocation settled the language, delivers the artifact with the map synchronised, and gives five unresolved findings.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — the contract's exception holds: an unusable recognized value stops the run *unless the Formal Invocation already settled that parameter*, and here it had. Genre and technique still came from the map.
  - `sync` — `pass` — the map comes back with `language: en_GB`, the value the run resolved, and `article` and `abt` unchanged; nothing else in the frontmatter moved.
  - `review` — `pass` — five findings, including one that the title asserts an outcome the body never reaches.
  - `anti-slop` — `pass` — the fourth finding names *it is worth noting that* as the apologetic opening the language's own anti-slop scope lists, which is the language scope reaching a finding rather than the shared catalogue alone.
  - `budget` — `pass` — `0`.
  - `findings` — `pass`.
  - `no-source` — `pass` — the third finding says the missing denominator *is not in the artifact* and that supplying it means going back to material *it is not the review's to invent*, which is the boundary stated from the right side of it.
  - `mechanics` — `pass` — once, found nothing.
  - `loading` — `pass` — `article`, `article.review`, `abt`, `abt.review`.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — five.
- **defects filed** — none.
- **notes** — read beside the run above, this pair is the whole of the unusable-metadata rule: the same file stops one run and not the other, and the difference is a single flag at level 1.

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/redline --genre=article --max=0 $RUN/corpus/frontmatter/frontmatter-unrelated.md -- Hold it to the ABT technique.`
- **contextual instruction** — `Hold it to the ABT technique.`
- **output target** — `response`
- **observed delivery** — a line resolving each parameter with its source, the complete artifact with its frontmatter byte-identical, seven unresolved findings, and a closing paragraph marked *Noted, not a finding* about the frontmatter's own contradictory keys.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — three parameters settled at three different levels in one invocation: `article` from the flag, `abt` from the Contextual Instruction, `en_GB` by inference from the text. This is as close as the corpus can come to the case the ticket names; see the note in **Run conditions**.
  - `sync` — `pass` — no `kntnt` map exists, so none was synchronised and none was added, and the document's own frontmatter comes back unchanged to the byte.
  - `review` — `pass` — seven findings against the selected genre, the selected technique, and the base contract.
  - `budget` — `pass` — `0`.
  - `findings` — `pass`.
  - `anti-slop` — `pass` — finding 6 names *than the literature suggests* as attribution to nobody and says it props up the draft's most contestable claim.
  - `no-source` — `pass`.
  - `mechanics` — `pass` — once, found nothing.
  - `loading` — `pass` — `article`, `article.review`, `abt`, `abt.review`.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — seven.
- **defects filed** — none.
- **notes** — the corpus's whole point here is the four bait keys sitting at the top level of ordinary frontmatter, and the run states the rule in the contract's own words before resolving anything: they sit outside a `kntnt` map, so they are the document's own fields. It then does the useful thing with them anyway — says they will be acted on by a publishing pipeline — while marking that as not a finding, which is the distinction the contract draws between what a review may say and what it may change.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/redline $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line stating the resolution and that no map was present or added, then the corrected text, then one line saying the source was not modified.
- **side effects** — none.
- **criteria** —
  - `sync` — `pass` — no map demanded, none added, and the delivered text opens directly on its heading as the fixture does.
  - `review` — `pass` — the correction repaired a synonym cycle between *roster* and *rota* and removed a closing superlative the text does not support.
  - `budget` — `pass` — one, spent once.
  - `fresh` — `pass`.
  - `verify` — `pass` — re-reviewed before the mechanical pass, which the narration marks as its own step.
  - `stop` — `pass` — clean after one round.
  - `no-source` — `pass`.
  - `mechanics` — `pass` — once, found nothing.
  - `loading` — `pass` — `general` only.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor is a demand for metadata, a refusal, or a map added by a Skill nobody asked to write one. None of the three.

## `frontmatter-absent` (inline)

- **fixture** — `frontmatter-absent`
- **invocation** — `/redline --max=0 ` followed by the fixture's complete text pasted in as inline material
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text back unchanged in a fenced block, the resolved configuration, and five unresolved findings, each closing with the requirement it is against.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — five findings on a text a file-supplied run had found two in, which is the range a review of competent prose leaves open rather than a disagreement about the contract.
  - `anti-slop` — `pass` — findings 2 and 3 name importance inflation, generic conclusions, and robotic rhythm, each with the catalogue's name attached and the instances quoted.
  - `budget` — `pass` — `0`.
  - `findings` — `pass`.
  - `sync` — `pass` — no map, none added.
  - `no-source` — `pass` — finding 4 says supplying a specific *would mean inventing one* and that the text needs material the draft does not carry, which is the boundary from the right side.
  - `mechanics` — `pass` — once, found nothing.
  - `loading` — `fail` — an incorrect reading: `general` was resolved and `genres/article.md` was read beside `genres/general.md`.
  - `target` — `pass` — response, and no file exists anywhere for this run to have touched.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — five.
- **defects filed** — #140.
- **notes** — this is the record's inline-supply entry. The corpus's inline fixture is `brief-short`, and the run of it is recorded below as a failure of a different kind, so inline supply is exercised here on material that is a Text Artifact rather than a brief. It reached the Skill and was reviewed exactly as the same text was when supplied as a path.

## `response-default`

- **fixture** — `response-default`
- **invocation** — every run in this record that named no `--output` and no `--in-place`; the fixture is a situation rather than material
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — in each case the result reached the response — the artifact, a short no-change status, a question, or a refusal — and no file was created anywhere.
- **side effects** — none, in every one of the twenty-five runs that named no destination. Each of their inventories is identical before and after.
- **criteria** —
  - `target` — `pass` — the default held whether the material was inline, a local path, or a URL. Reading a file selected no destination in any run, and no run offered to write one.
  - `effects` — `pass` — the corpus's rejection here is any file created, replaced, or removed under the working copy by a run that named no destination, and no such run touched anything under it.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — several runs wrote a scratch file outside the working copy, in the system temporary directory, to hand a correction brief to a subagent. None of them was the artifact, none was under the working copy, and all but one were removed by the run that made them. It is recorded because a later reader checking only the working copy would not see that `/tmp` was touched at all, and because the way that handover is done is itself #143.

## `new-file`

- **fixture** — `new-file`
- **invocation** — `/redline --output=$RUN/out/reviewed.md $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/reviewed.md`
- **observed delivery** — one line naming the file that received the artifact, then the resolved configuration, the round spent, and a statement that the re-review found nothing remaining. The text was not repeated.
- **side effects** — `out/reviewed.md` created. Nothing else; the source is byte-identical to the corpus.
- **criteria** —
  - `target` — `pass` — exactly the named path was created, it holds the complete artifact, and the response did not repeat it.
  - `effects` — `pass` — one file created, and it is the one named.
  - `review` — `pass` — two findings, each naming the requirement it is against: a missing step between the diagnosis and the rewrite, which is the step the title undertakes to supply, and a stock opening sentence carrying no information.
  - `budget` — `pass` — one, spent once.
  - `fresh` — `pass` — the brief the subagent received carries the complete text as it then stood, both findings in full with their requirement citations, the resolved parameters, and the instruction to leave a finding alone rather than repair it by inventing a fact.
  - `verify` — `pass` — the returned text was reviewed again and found clean before the mechanical pass.
  - `stop` — `pass` — stopped on no findings after one round, with nothing carried forward.
  - `findings` — `pass` — none left, and the run says so.
  - `no-source` — `pass` — the first finding says the answer is already in the artifact, in paragraphs one and four, and nothing asks for material outside it.
  - `mechanics` — `pass` — once, after the correction.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `general` only.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the correction added two sentences — *We could have patched that retry. But a patch fixes the behavior you found, and nobody could account for the rest of what the importer was doing.* — which is an addition rather than a deletion or a narrowing, and is recorded as such so a later reader can judge it. It is not an unsupported fact: the finding it repairs says explicitly that the answer is already in the draft, in *five other things nobody had documented* and *a component nobody can explain*, and never used where the argument turns, and the added sentences carry that material to the turn. Nothing about the world entered that the artifact did not already hold. Two other runs of this same fixture met the same gap and left it standing as unrepairable, which is the range this record can honestly report on it. This fixture's first run is recorded under **Runs discarded**; this entry is the re-run made on its own.

## `existing-file`

- **fixture** — `existing-file`
- **invocation** — `/redline --output=$RUN/corpus/output/existing-target.md $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — the resolved configuration, a paragraph saying what the review had judged and found nothing substantive in, the complete list of mechanical corrections, and one line naming the file that received the artifact and saying the occupant was replaced.
- **side effects** — `corpus/output/existing-target.md` replaced. Nothing created beside it, and the source file is byte-identical to the corpus.
- **criteria** —
  - `target` — `pass` — the occupant is gone and the exact named file holds the artifact. No confirming flag was asked for and none was offered, which is what the contract says naming an existing path means.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
  - `review` — `pass` — no substantive finding, and the run says what it judged to reach that: the angle, the paragraph sequence, the connectives, the arithmetic of eleven as eight plus three, the strength of the claims, and each anti-slop pattern by name. It also says why the one negated construction is not a false contrast — it corrects a belief the preceding paragraphs genuinely create — which is the catalogue's own exception applied rather than the pattern matched on shape.
  - `anti-slop` — `pass` — named and checked individually on a text that carries none.
  - `budget` — `pass` — the default `1` went unspent, because there was nothing to spend it on.
  - `stop` — `pass` — stopped on no findings with the budget unspent.
  - `mechanics` — `pass` — once, and it is the whole of what changed: fourteen corrections, with the American spellings kept and the consistently spaced em dashes and the contrastive comma splice left alone as the text's own established choices.
  - `findings` — `pass` — none to deliver, and the run says so.
  - `no-source` — `pass`.
  - `sync` — `pass` — no map, none added.
  - `loading` — `fail` — an incorrect reading: `general` was resolved and `genres/article.md` and `genres/article.review.md` were read beside `genres/general.md`.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — #140.
- **notes** — the corpus rejects a demand for an extra confirming flag, a sibling written beside the occupant, and the occupant left in place while the result went elsewhere. None of the three. The file this run wrote is byte-identical to the one the `existing-directory` run wrote from the same source, which is worth a later reader's attention: two independent runs reached the same mechanical result on this fixture, while a third found two substantive defects in it as well. This fixture's first run is recorded under **Runs discarded**; this entry is the re-run made on its own.

## `existing-directory`

- **fixture** — `existing-directory`
- **invocation** — `/redline --output=$RUN/out $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — one line saying the review found no substantive defect, that the budget therefore went unspent, and that the mechanical pass ran once, then the path the artifact went to and the resolved configuration.
- **side effects** — `out/flawed-en-US.md` created. Nothing else.
- **criteria** —
  - `target` — `pass` — the name was derived from the source basename, kept the source's extension, and landed inside the named directory and nowhere else.
  - `effects` — `pass` — one file created, in the directory that was named.
  - `review` — `pass` — no substantive finding, on a text two other runs found one or two in. The corpus asserts nothing about which is right, and a review of competent argument leaving it alone is inside the contract.
  - `budget` — `pass` — unspent, because there was nothing to spend it on.
  - `stop` — `pass` — no findings, budget unspent.
  - `mechanics` — `pass` — once. The written file carries the mechanical repairs and keeps `normalize` and `catalog`, which is the resolved `en_US` reaching the mechanics.
  - `findings` — `pass` — none to deliver.
  - `no-source` — `pass`.
  - `sync` — `pass` — no map, none added.
  - `loading` — `fail` — an incorrect reading: `general` was resolved and `genres/article.md` was read beside `genres/general.md`.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — #140.
- **notes** — the corpus rejects a file named for the directory rather than derived from the source, a derived name with no suitable text extension, and anything written outside the named directory. None of the three. This is also the entry that shows an unchanged-looking run still creating the file: the review changed nothing substantive, and the file was created anyway because creating it was what the invocation asked for.

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/redline --output=$RUN/corpus/output/collision $RUN/corpus/output/interview-notes.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the resolved configuration, then an explanation that the derived name and its `-2` sibling were taken and the result went to the first free candidate, naming the path; then an account of the two findings and the one correction round.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants are byte-identical to the corpus, and so is the source.
- **criteria** —
  - `target` — `pass` — the stem stayed `interview-notes`, the candidate taken was the first free one in ascending order, and it is inside the named directory.
  - `effects` — `pass` — exactly one file created and nothing else touched; the corpus's rejection is either occupant overwritten and a name built by suffixing the colliding candidate, and neither happened.
  - `review` — `pass` — two findings: the opening paragraph running a workload point and a staffing point together, and a sentence stating two facts in the order that puts the surprise ahead of its cause.
  - `budget` — `pass` — one, spent once.
  - `fresh` — `pass`.
  - `verify` — `pass` — the re-review found nothing left and the loop stopped there rather than at the budget.
  - `stop` — `pass` — stopped on no findings, with the round spent and nothing carried forward.
  - `mechanics` — `pass` — once, and its one change was quotation marks around a word used as a word.
  - `findings` — `pass` — none left.
  - `no-source` — `pass` — the interview behind the notes is never asked for.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `general` only.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the correction rewrote *took the course … and volunteered for it, which Halldin says surprised her* as *volunteered … and took it. Halldin says their volunteering surprised her*, which settles a referent the original leaves open. It is recorded because pinning an ambiguous referent is an interpretation as well as a repair; the interpretation it chose is the one the sentence's own *volunteered for it* supports, and nothing was added.

## `read-only-source`

- **fixture** — `read-only-source`
- **invocation** — `/redline --in-place $RUN/corpus/output/readonly-source.md`
- **contextual instruction** — `none`
- **output target** — In-place Editing
- **observed delivery** — a refusal naming the file's mode, the synopsis verbatim, the help pointer, a sentence saying nothing was reviewed and nothing written, and the two invocations that would work instead.
- **side effects** — none. The file's mode is unchanged and its content is byte-identical.
- **criteria** —
  - `refusal` — `pass` — In-place Editing requires a writable local file, and the refusal says so, prints the synopsis, and points at help.
  - `effects` — `pass` — the corpus's three rejections are a permission changed to make the write possible, a result written elsewhere as a silent substitute, and a partial effect left behind. None of the three: the mode is untouched, nothing was written anywhere, and the review never started.
  - `review` — `skipped` — the refusal is settled by reading before anything is reviewed, which is what the contract asks for so that a refusal has nothing behind it.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `in-place-request`

- **fixture** — `in-place-request`
- **invocation** — `/redline --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — In-place Editing
- **observed delivery** — one line saying the file had been replaced, the resolved configuration, an account of the one correction and its verification, and the single change named exactly.
- **side effects** — `corpus/output/in-place-source.md` replaced. Nothing created beside it, and nothing else in the working copy moved.
- **criteria** —
  - `target` — `pass` — the one file the contract allows to be replaced was replaced, on an explicit request, and no copy was left beside it.
  - `effects` — `pass` — exactly one file changed, and it is the source.
  - `review` — `pass` — one finding, repaired: an absolute clause the paragraph does not support.
  - `budget` — `pass` — one, spent once.
  - `fresh` — `pass`.
  - `verify` — `pass` — the run says the returned text was verified by a fresh review.
  - `stop` — `pass` — clean after one round.
  - `mechanics` — `pass` — once, found nothing.
  - `findings` — `pass` — none left.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `general` only.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's third rejection here is a rewritten file where the run found nothing to change and a short status was the contract. It does not apply: this run found something and changed it, so replacing the file is what the request bought. The unchanged in-place case is not staged by this corpus and is not claimed by this record.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/redline --output=$RUN/corpus/output/in-place-source.md $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — the source path, named separately
- **observed delivery** — a refusal saying `--output` names the same path as the Text Artifact and that replacing a source is requested with `--in-place`, the synopsis, the help pointer, and a sentence saying nothing was reviewed and nothing written.
- **side effects** — none. The file is byte-identical to the corpus.
- **criteria** —
  - `refusal` — `pass` — refused, and the refusal points at In-place Editing, which is the one recognisable authorisation the contract keeps for replacing a source.
  - `effects` — `pass` — the file was not replaced and nothing was created.
  - `review` — `skipped` — settled by reading, before anything was reviewed.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/redline --output=$RUN/out/x.md --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — a file and In-place Editing, at once
- **observed delivery** — a refusal saying both were given and that they name two destinations for one text, noting that bare `--in-place` means `on`, then the synopsis and the help pointer.
- **side effects** — none. `out/` is empty and the named source is byte-identical to the corpus.
- **criteria** —
  - `refusal` — `pass` — the mutual exclusion is stated as the reason, and the refusal reads the bare flag as `on` before applying it, which is the vocabulary the contract defines.
  - `effects` — `pass` — the corpus's rejection is either half executed. Neither was: no file at the named path, and the source untouched.
  - `review` — `skipped` — settled by reading.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `url-source` (In-place Editing refused)

- **fixture** — `url-source`
- **invocation** — `/redline --in-place https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — In-place Editing
- **observed delivery** — a refusal saying In-place Editing requires exactly one writable local file and that fetching a URL grants no right to write anything back, then the synopsis, a line saying nothing was fetched, reviewed, or written, the help pointer, and the two invocations that would work.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — this is the corpus's first rejection for the fixture and it was refused, with the reason stated in terms of what a URL is rather than as a rule recited.
  - `effects` — `pass` — nothing under the working copy moved, and the run says it did not even fetch, which is the refusal being settled by reading as the contract requires.
  - `review` — `skipped` — nothing reviewed, correctly.
  - `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `url-source` (reviewed, filename derived from the URL)

- **fixture** — `url-source`
- **invocation** — `/redline --max=0 --output=$RUN/out https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the resolved configuration, the path the artifact went to, seven unresolved findings, and a list of the mechanical corrections applied in the delivered text.
- **side effects** — `out/key-words-for-use-in-rfcs-to-indicate-requirement-levels.txt` created. Nothing else.
- **criteria** —
  - `target` — `pass` — the name was derived from the document's own title rather than from a basename, since a URL has no useful one, and it kept a suitable text extension and landed inside the named directory.
  - `effects` — `pass` — one file created, in the directory named.
  - `review` — `pass` — seven findings against the artifact itself, the strongest of them a contradiction inside the document: the boilerplate the abstract prescribes binds ten terms and section 4 defines an eleventh that is not in it.
  - `budget` — `pass` — `0`.
  - `findings` — `pass` — all seven in the response beside the file.
  - `no-source` — `pass` — the corpus's second rejection is a definition attributed to the RFC that the RFC does not give, and every finding quotes the document.
  - `mechanics` — `pass` — once.
  - `sync` — `pass` — no map, none added.
  - `loading` — `fail` — an incorrect reading: `general` was resolved and `genres/report.md` was read beside `genres/general.md`.
  - `leak` — `pass`.
- **unresolved findings** — seven.
- **defects filed** — #140.
- **notes** — the mechanical pass reported eleven corrections to the RFC's own text. One of them, `mean` → `means` in the five definition entries, is a judgement call rather than an error: the subject is a disjunction — *This word, or the terms "REQUIRED" or "SHALL", mean…* — and agreement with the nearer conjunct is standard. It is recorded here rather than filed, because it is a decision of the mechanical pass and Proofread's own evaluation is issue #107's; a later reader comparing this run with a GPT-family one should compare the eleven rather than the count.

## `factual-source-long`

- **fixture** — `factual-source-long`
- **invocation** — `/redline --genre=report --max=0 $RUN/corpus/source/factual-source-long.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line saying what the review was read against, that the budget was `0`, and that the mechanical pass found nothing, then nine unresolved findings, then the artifact unchanged.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — nine findings on eight hundred words, and the second is the one this fixture is really for: the 2024 boarding breakdown sums to 393,400 against a stated total of 412,000, while the 2023 pair reconciles exactly. That is arithmetic on the artifact's own numbers, which is the kind of finding the contract keeps and the kind a review that only reads for style never reaches.
  - `no-source` — `pass` — this is the record's hardest case for the criterion, because the fixture *is* source material and its closing section names its own limits. Nothing in the review asks for material behind it, and nothing remarks that verification was unavailable; the findings that concern missing facts say the document does not carry them and name what it would take to close each.
  - `budget` — `pass` — `0`.
  - `findings` — `pass` — all nine delivered and marked unresolved.
  - `precedence` — `pass` — `report` from the flag, `en_GB` by inference, no technique.
  - `mechanics` — `pass` — once, and it names what it checked in a text full of dates, thousands separators, and *per cent*: nothing to correct.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `report` and `report.review`, nothing else.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — nine.
- **defects filed** — none.
- **notes** — the corpus's rejections for this fixture are written for a Skill drafting from it — a causal claim about one of the three simultaneous changes, the satisfaction figure read as the catchment's, the seventeen missing counting days read as zero, and any number not in the source. A review makes no claims of its own, so none of the four can be committed here; what the run does instead is name the ferry service opened during the trial as an unquantified alternative explanation disclosed twenty lines after the comparison it qualifies, which is the same hazard seen from the reviewing side.

## `brief-article-abt`

- **fixture** — `brief-article-abt`
- **invocation** — `/redline --genre=article --technique=abt --max=0 $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the resolved configuration, the artifact unchanged, and five unresolved findings, the first of them that the artifact is a brief and not the article it commissions.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — the review judged what was in front of it. It named the material as a brief, said every finding below follows from that, and then held the text to the selected genre and technique anyway: it identifies the ABT arc the material holds, quotes each of its three parts, and says the fault is that all three sit inside one 87-word paragraph so the complication never bites.
  - `precedence` — `pass` — genre and technique from the flags, `en_GB` by inference.
  - `budget` — `pass` — `0`.
  - `findings` — `pass`.
  - `no-source` — `pass` — the first finding says repairing it *means writing the article, which is not a review's work*, and nothing asks for material.
  - `mechanics` — `pass` — once, found nothing.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `article`, `article.review`, `abt`, `abt.review`.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — five.
- **defects filed** — none.
- **notes** — the corpus supplies this fixture to a Skill that drafts, and its rejections are about a draft: an attribution Miriam Adler did not make, the two stated limits dropped, a piece unrecognisable as the genre. None can be committed by a review that changes nothing, and this run committed none of them. It is recorded rather than skipped because the fixture is what exercises a selected genre and a selected technique reaching a Redline review, and because it is the control for the failure recorded under `brief-short` below.

## `brief-report-pac`

- **fixture** — `brief-report-pac`
- **invocation** — `/redline --genre=report --technique=pac --max=0 $RUN/corpus/source/brief-report-pac.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the resolved configuration, the artifact unchanged, and seven unresolved findings.
- **side effects** — none.
- **criteria** —
  - `review` — `pass` — held to the report genre and the PAC technique: the premise is identified as sound and stated first, and the findings are that it is never tested, that no answer appears, and that the text ends on a scheduling fact rather than a conclusion.
  - `precedence` — `pass` — both from the flags, `en_GB` by inference.
  - `budget` — `pass` — `0`.
  - `findings` — `pass`.
  - `no-source` — `pass` — the first finding says writing the missing report *is composition* and outside what a correction may add.
  - `mechanics` — `pass` — once, found nothing.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `report`, `report.review`, `pac`, `pac.review`.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — seven.
- **defects filed** — none.
- **notes** — the corpus's rejection here is a draft that resolves the on-call lead's counter-argument by inventing evidence for or against it. The review did not resolve it and did not supply any: it records that the objection is put and never examined, which is a finding about the text rather than an answer to the objection.

## `brief-press-release-sv`

- **fixture** — `brief-press-release-sv`
- **invocation** — `/redline --genre=press-release --max=0 $RUN/corpus/source/brief-press-release-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a header line in Swedish giving the resolved genre, technique, language, and budget, a line saying the mechanical pass found nothing, the artifact unchanged, and findings in Swedish.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `sv` by inference with no flag, and the whole of the review is in Swedish.
  - `precedence` — `pass` — `press-release` from the flag, language by inference, no technique.
  - `review` — `pass` — the findings are the genre's own: the first sentence carries an instruction rather than the news, and the sentence that does carry it is the text's fourth.
  - `budget` — `pass` — `0`.
  - `anti-slop` — `skipped` — Swedish material carrying none of the patterns; see #142.
  - `findings` — `pass`.
  - `no-source` — `pass`.
  - `mechanics` — `pass` — once, found nothing.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `press-release` and `press-release.review`.
  - `target` — `pass`.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — the review's, all unresolved at `--max=0`.
- **defects filed** — none.
- **notes** — the corpus's rejection is a draft in any language but Swedish where nothing overrode inference, and any suggestion that the workshop repairs devices for visitors or sells parts. The review changed nothing and asserted neither. This is the record's second run of a Swedish inference with no flag in play, and both reached `sv`.

## `brief-short` (inline)

- **fixture** — `brief-short`
- **invocation** — `/redline ` followed by the fixture's complete text pasted in as inline material, as the corpus asks
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no review. The run said the operand is a brief rather than a draft, that reviewing it literally would be nonsense, proposed a `/write` invocation with flags, asked two questions about locale and genre, offered to run both passes in sequence, and closed with an editorial opinion about which two lines of the brief a draft should keep prominent.
- **side effects** — none.
- **criteria** —
  - `refusal` — `fail` — an unresolved mandatory finding, in the sense the protocol names: the contract requires a supplied Text Artifact to be reviewed and its findings to be delivered or reported, and this run delivered neither. The invocation is valid by the Skill's own `## Arguments` — one operand, inline text, no flags — and the refusal is not one of the forms that section lists.
  - `review` — `fail` — nothing was reviewed.
  - `loading` — `fail` — nothing the contract names was loaded, and `write/SKILL.md` and `write/help.md`, which it does not name, were.
  - `effects` — `pass` — nothing was written, which is the one thing that held.
  - `leak` — `pass` — vacuously; there was no review to leak.
- **unresolved findings** — none delivered, which is the failure.
- **defects filed** — #141.
- **notes** — the same Skill does the right thing with the same kind of material supplied as a path: the three brief fixtures above were each reviewed, and each made *this is a brief and not what it commissions* its first finding. That is why this is recorded as a deviation rather than as a property of the material. The corpus's own rejection for this fixture — a draft reporting a benefit the brief does not contain — cannot be committed by a run that produces no text, and is not what failed here.

## `interview-transcript`

- **fixture** — `interview-transcript`
- **invocation** — not run
- **contextual instruction** — `none`
- **output target** — `none`
- **observed delivery** — none.
- **side effects** — none.
- **criteria** —
  - all — `skipped` — the fixture is source material for a Skill that drafts. Its corpus entry says to supply it *as source material for a draft that quotes the speaker*, and every one of its rejections judges what a direct quotation does to spoken material: information added, stance or certainty changed, a self-correction removed, distinctive wording smoothed away inside quotation marks. Redline never compares an artifact with source material and produces no quotations, so none of them can be committed by any run of it. The fixture is the one piece of corpus material whose whole content is a situation this Skill's contract puts outside itself.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — recorded rather than omitted, because a fixture missing from a record reads later as a fixture that passed. The nearest thing to it that this Skill does meet — a text carrying quoted speech — is `derived-name-collision`'s `interview-notes.md`, which was reviewed and corrected, and whose one quoted word survived the mechanical pass with quotation marks added around it.

## `<negative Correction Budget>`

- **fixture** — none; the invocation is the case
- **invocation** — `/redline --max=-1 $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a one-line refusal saying `--max=-1` is not a non-negative integer and that nothing was reviewed or written, the synopsis verbatim, and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the option is refused before anything is reviewed or written, which is what the contract asks of a malformed value, and the refusal names the value rather than the option in general.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus has no fixture for this because it is a property of the invocation rather than of any material; it is recorded because the acceptance criteria ask that an invalid Correction Budget be refused before side effects, and this is the cheapest place to see it.

## `<uninstalled genre>`

- **fixture** — none; the invocation is the case
- **invocation** — `/redline --genre=novella $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a refusal naming the genre as not installed and listing the four that are — `article`, `general`, `press-release`, `report` — then the synopsis, the help pointer, and a line saying nothing was reviewed and nothing written.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — refused rather than falling back to the default, and the refusal reads the installed set off the directory rather than off a list kept somewhere else, which is what makes adding a genre a matter of adding a file.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## Criteria the corpus could not stage on its own

Three of this ticket's acceptance criteria name situations the shared corpus has no material for, and a criterion left unjudged is not a result. They are judged here, in seven further invocations made after the thirty-six above, one at a time with nothing else in flight, under the same install, the same harness, and the same before-and-after inventory.

Nothing in the corpus was changed to close them. Two of the three are staged on run-local probe material, reproduced in full below and staged into each throwaway working copy as `$RUN/probe/` beside `$RUN/corpus/`; the corpus commit those entries name is still `6d476db`, because no fixture, no index entry, and no `Reject` line was touched. The third needed no new material at all: it is staged on corpus fixtures held to a genre they are not written in. The corpus's own gap — no Swedish fixture carrying concentrated slop, and no partial `kntnt` map — is real and stays open as #142; probe material judges the Skill without pretending the corpus can.

Probe material is quoted here rather than described so that a GPT-family run can reproduce it exactly, which is what the recording format exists for.

### `probe/partial-map-sv.md`

An internal note in Swedish about dropping a daily stand-up, carrying a `kntnt` map with one key. It is not a press release and does not resemble one, so a `genre` of `press-release` can only have come from the map.

```markdown
---
kntnt:
  genre: press-release
---

# Vi slutade med den dagliga avstämningen

Utvecklingsgruppen hade ett stående möte varje morgon klockan nio. Det tog femton minuter när det gick fort och trettiofem när någon hade fastnat i något. I januari bytte vi det mot en skriven uppdatering i den kanal där arbetet ändå diskuteras.

Regeln är att den som har något som blockerar skriver det före klockan tio, och att den som kan lösa det svarar i tråden. Allt annat får ligga. Vi bokar ett möte först när tråden har gått fram och tillbaka två gånger utan att landa.

Sedan bytet har fyra personer bett om att få tillbaka mötet och tre av dem har ändrat sig efter en månad. Vi har inte mätt om något blir klart snabbare, och vi tror inte att det är det bytet handlar om. Det vi vet är att förmiddagen numera börjar när var och en väljer att börja den.
```

### `probe/partial-map-en.md`

An English note about a duplicated monitoring contract, carrying a `kntnt` map with one key — a different key from the fixture above, so that the three sources are not always in the same roles. Its money is written in dollars and its spelling leans American, so an `en_GB` locale can only have come from the invocation.

```markdown
---
kntnt:
  technique: pac
---

# The second monitoring contract

We have paid for two monitoring services since March. The older one covers 41 hosts and costs $1,180 a month. The newer one covers 38 of the same hosts and costs $940 a month, and it was signed while the first contract was still inside its notice period.

Over the last twelve months the two services raised 214 alerts between them. 197 of those were raised by both. Of the 17 raised by only one service, 11 came from the older one and 6 from the newer, and none of the 17 turned out to be an incident that the other service missed for longer than four minutes.

The access log shows that nobody has opened the newer service's dashboard since May. The argument for keeping it is that two providers do not fail together, and we have no evidence either way about that: no monitoring outage has occurred in the period the log covers.
```

### `probe/slop-sv.md`

A Swedish counterpart to `slop-heavy`: the same catalogue patterns in concentration, written as Swedish rather than translated from the catalogue's English examples, and carrying the tells the Swedish language resource's own anti-slop scope names — the stock metaphor set, the triad reflex, the superlative run, the connective adverb with an English comma after it, the unspaced em dash, and English curly quotation marks. One paragraph carries real material, so that a correction which removes the patterns and the content with them is visible as such.

```markdown
# Medarbetarsamtalet i en ny tid

I dagens snabbrörliga arbetsliv har medarbetarsamtalet aldrig varit viktigare. Det är värt att notera att allt fler organisationer nu ser över hur de arbetar med återkoppling.

Det handlar inte om att fylla i en blankett—det handlar om att skapa en genuin dialog. Frågan är inte om samtalet ska förändras, utan när. Utvecklingssamtalet är inte bara ett administrativt moment. Det är hörnstenen i modernt ledarskap.

Studier visar att medarbetare som får regelbunden återkoppling presterar bättre. Experter menar att den årliga cykeln har spelat ut sin roll. Det är allmänt känt att engagemang hänger nära samman med upplevd delaktighet. Som en av våra chefer uttryckte det: “Det viktigaste är att lyssna.”

Den nya modellen är revolutionerande. Den är banbrytande. Den är helt avgörande för framtidens arbetsplatser. Dessutom, är det viktigt att komma ihåg att resan mot en feedbackkultur tar tid, och att nyckeln till framgång ligger i att verkligen förstå kraften i den kontinuerliga dialogen.

Samtalet ska vara snabbt, enkelt och säkert. Dialogen ska vara öppen, ärlig och konstruktiv. Utvecklingssamtalet ska vara tydligt, tryggt och tillgängligt.

Chefen bokar ett möte. Chefen ställer frågor. Chefen antecknar. Medarbetaren svarar. Medarbetaren reflekterar. Medarbetaren går vidare.

Vår HR-avdelning genomförde 412 medarbetarsamtal under 2025. Trettioåtta procent av dem hölls efter årsskiftet, eftersom sjukfrånvaron i november och december var högre än vanligt. Vi har inte mätt om de samtal som sköts upp skilde sig i innehåll från de övriga.

Vidare, understryker detta betydelsen av ett systematiskt arbetssätt som tar tillvara hela organisationens engagemang för sina medarbetare.

Sammanfattningsvis handlar det i slutändan om att våga se varandra. Är inte det egentligen vad ett medarbetarsamtal alltid har handlat om? Framtiden får utvisa vart resan bär.
```

## `<three sources, three parameters, one invocation — Swedish>`

- **fixture** — none; run-local `probe/partial-map-sv.md`, reproduced above
- **invocation** — `/redline --language=sv --max=0 $RUN/probe/partial-map-sv.md -- Hold it to the ABT technique.`
- **contextual instruction** — `Hold it to the ABT technique.`
- **output target** — `response`
- **observed delivery** — one line naming each parameter and the level it came from, then the artifact with its one-key map completed to three, then six findings in Swedish, all marked unresolved.
- **side effects** — none. The inventory is identical before and after.
- **criteria** —
  - `precedence` — `pass` — the criterion in the form the ticket names it, inside one invocation: *Reviewed as **press-release** (from the artifact's `kntnt` map) against the **ABT** technique (from your instruction), in **Swedish***. The flag settled the language, the map settled the genre, and the Contextual Instruction settled the technique, and no two of them settled the same parameter. Two of the three are decidable against the level below as well: `press-release` is not what inference would give an internal note, and a technique is never inferred at all.
  - `sync` — `pass` — the map arrives carrying `genre` alone and comes back carrying `genre: press-release`, `technique: abt`, `language: sv`, which is what the run resolved. The body is unchanged and the frontmatter holds nothing else to leave alone.
  - `language` — `pass` — the findings are written in Swedish and the mechanical pass resolved the `mechanics` scope for `sv`.
  - `review` — `pass` — six findings: three against the press-release genre, two against ABT, one against the base contract's register, each naming where and what the reader loses.
  - `budget` — `pass` — `0`; nothing was delegated and the trace carries no `Task`.
  - `anti-slop` — `skipped` — competent Swedish carrying none of the patterns. The run says so explicitly; the Swedish half of that criterion is judged two entries below.
  - `no-source` — `pass` — findings 2 and 3 say the *artifact* carries no printable fact and no contact, and that the missing values must not be invented. Nothing asks for material and nothing remarks that verification was unavailable.
  - `mechanics` — `pass` — `proofread/SKILL.md` read once and the `mechanics` scope resolved once, both after the review; the pass found nothing.
  - `findings` — `pass` — six delivered beside the artifact, all marked unresolved.
  - `loading` — `pass` — `press-release.md`, `press-release.review.md`, `abt.md`, `abt.review.md`, and nothing else from either directory.
  - `target` — `pass` — no destination named; the response received the artifact.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — six.
- **defects filed** — none.
- **notes** — the run also volunteers, under finding 1, that four of its six findings follow from the genre the map named and that a `--genre=` would produce a different review. That is the precedence rule stated from the inside, and it is what a reader of a map-configured review needs to know.

## `<three sources, three parameters, one invocation — English>`

- **fixture** — none; run-local `probe/partial-map-en.md`, reproduced above
- **invocation** — `/redline --language=en_GB --max=0 $RUN/probe/partial-map-en.md -- Treat it as an internal report to the board.`
- **contextual instruction** — `Treat it as an internal report to the board.`
- **output target** — `response`
- **observed delivery** — a line attributing each parameter to its level, then the artifact with its map completed, then seven findings, all unresolved.
- **side effects** — none.
- **criteria** —
  - `precedence` — `pass` — the same criterion with the three sources rotated into different roles, and the run names them itself: *genre `report` from the contextual instruction, language `en_GB` from the flag, technique `pac` from the map*. Read beside the entry above, the pair shows the independence is per parameter rather than an artefact of one arrangement.
  - `sync` — `pass` — the map arrives carrying `technique` alone and comes back carrying `technique: pac`, `genre: report`, `language: en_GB`. Nothing else in the frontmatter exists to change, and the body is unchanged.
  - `language` — `pass` — the flag beat the artifact's own leaning rather than agreeing with it: finding 5 raises the unstated currency behind `$1,180` *in a British-English document*, and the mechanical pass resolved the `mechanics` scope for `en_GB`.
  - `review` — `pass` — seven findings, the sharpest of them a real defect inside the artifact: the twelve-month comparison may not cover a period in which both services ran, because the arrangement is dated to an undated *March*, which would make the 214/197/17 split an artefact of unequal coverage.
  - `budget` — `pass` — `0`.
  - `anti-slop` — `skipped` — the text carries none of the patterns.
  - `no-source` — `pass` — the findings say what the *artifact* does not settle and never ask for the material behind it.
  - `mechanics` — `pass` — once, after the review, and it found nothing.
  - `findings` — `pass` — seven delivered, all unresolved.
  - `loading` — `pass` — `report.md`, `report.review.md`, `pac.md`, `pac.review.md`, and nothing else.
  - `target` — `pass` — the run closes by saying nothing was written to disk, which the inventory confirms.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — seven.
- **defects filed** — none.
- **notes** — this run is also the counter-case to #141. There, a Contextual Instruction naming a genre, a technique, and a language that a complete map had already settled was refused as inert. Here an instruction naming a parameter the map does not carry is applied rather than refused, which is what the precedence rule asks for and what makes the earlier refusal a defect rather than a policy.

## `<Swedish slop, review only>`

- **fixture** — none; run-local `probe/slop-sv.md`, reproduced above
- **invocation** — `/redline --max=0 $RUN/probe/slop-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a configuration line in Swedish, the artifact with the mechanical pass's Swedish punctuation applied, then fifteen findings in Swedish, all unresolved.
- **side effects** — none.
- **criteria** —
  - `anti-slop` — `pass` — all seven of the catalogue's patterns are found in Swedish, by name and on Swedish instances rather than on the catalogue's English strings: *tom öppning* for the empty opening, *staplade falska motsatser* for three false contrasts quoted individually, *uppblåst betydelse* for the superlative run, *tom källhänvisning* for three unattributed claims and the unnamed quotation, *synonymväxling* for the four names one thing carries, *mekanisk rytm* for the six identically built sentences, and *generisk avslutning* for four closing formulas in three sentences. Two further findings come from the Swedish resource's own anti-slop scope rather than from the shared catalogue — the stock metaphor set and the triad reflex — which is the language scope reaching a finding on its own.
  - `review` — `pass` — fifteen findings, each located in a numbered paragraph, and the four that are not anti-slop are real: no stated reader, an unintroduced *den nya modellen*, the only checkable material buried second from last, and a *Vidare understryker detta* whose *detta* is a paragraph that says the thing was not measured.
  - `language` — `pass` — inferred `sv` with nothing naming it, and the whole reply is in Swedish.
  - `budget` — `pass` — `0`; nothing delegated.
  - `mechanics` — `pass` — once, after the review, and it did work the review had not done: the unspaced em dash became a spaced en dash, the English curly quotation marks became Swedish `”…”`, and the English comma after *Dessutom* and *Vidare* went. Those are Swedish mechanics, and a run with `--max=0` is still entitled to them.
  - `no-source` — `pass` — finding 4 says the three claims *cannot be checked or contradicted*, which is a judgement about the artifact, and nothing anywhere asks for the material behind it.
  - `findings` — `pass` — fifteen delivered, all marked unresolved because the budget was zero.
  - `sync` — `pass` — no `kntnt` map, and none added.
  - `loading` — `pass` — `general.md` alone; no technique, and no genre resource read that the run did not resolve.
  - `target` — `pass` — the run states that `slop-sv.md` is unchanged on disk, and the inventory agrees.
  - `effects` — `pass`.
  - `leak` — `pass`.
- **unresolved findings** — fifteen.
- **defects filed** — none.
- **notes** — this is the entry that settles the second half of the anti-slop criterion. The catalogue says in its own opening that its examples are English and are patterns rather than strings, to be applied *by what each one does in the target language*; this run does that, on material whose instances share no wording with the examples. It is run-local material and not corpus material, so it says something about the Skill and nothing about the corpus, whose gap is still #142.

## `<Swedish slop, one correction>`

- **fixture** — none; run-local `probe/slop-sv.md`, reproduced above
- **invocation** — `/redline --language=sv --max=1 $RUN/probe/slop-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a corrected Swedish text of one paragraph, then a note of what the round repaired and three findings left standing.
- **side effects** — none.
- **criteria** —
  - `anti-slop` — `pass` — the first review recorded eleven findings and named the patterns in its own brief: F2 the empty opening, F3 vague attribution three times in one paragraph, F4 importance inflation with the stock metaphor, F5 stacked false contrasts, F6 the triad reflex and robotic rhythm, F7 synonym cycling, F9 the generic conclusion. Ten of the eleven were repaired.
  - `budget` — `pass` — `1`, spent once, and the trace carries exactly one `Task`.
  - `fresh` — `pass` — one subagent started fresh, whose whole instruction was the filled-in brief: 318 words of complete current text and all eleven findings, complete and in the order recorded.
  - `verify` — `pass` — the three findings delivered are the review that followed the correction, not the corrector's account of itself; one of them is a defect the correction itself created, the orphaned sjukfrånvaro sentence left behind when the unsupported causal wording went.
  - `stop` — `pass` — the budget was spent with findings left, the third of the three conditions, and they were carried forward as unresolved.
  - `language` — `pass` on the half the contract settles: `sv` reached the review, the delivered artifact is Swedish, and the mechanical pass ran in Swedish. See the notes for the half it does not settle.
  - `review` — `pass`.
  - `no-source` — `pass` — finding 1 says giving the text something to say *requires material the draft never contained*, and that supplying it would mean inventing facts. That is the boundary stated from the right side of it.
  - `mechanics` — `pass` — once, after the correction, and it found nothing.
  - `findings` — `pass` — three delivered with the artifact, each marked unresolved with a reason.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `general.md` alone.
  - `target` — `pass`. `effects` — `pass`. `leak` — `pass`.
- **unresolved findings** — three: the text has no job and no claim, the title promises a change the surviving prose does not describe, and the sjukfrånvaro sentence is now orphaned.
- **defects filed** — #145.
- **notes** — two things a later reader needs. The correction cut about 280 words to about 60, which is the same shape as the `--max=1` run on `slop-heavy` and stays on the same side of the line: what went was the empty opening, the three unattributed claims, the superlative run, the adjective triads, the six parallel sentences, the closing formulas, and the quotation attributed to *en av våra chefer* — deletion being the catalogue's own prescribed repair for an unsourced claim, which it forbids furnishing with a source — and the one paragraph the draft actually supported came back whole. The corrector named the quotation as the deletion worth a second opinion, unprompted. And the findings report came back in English for a Swedish artifact, where the `--max=0` run on the same text reported in Swedish; nothing in `SKILL.md` or `delivery.md` says which language a findings report is written in, though `delivery.md` settles it for the no-change status. That is #145.

## `frontmatter-absent` (press-release genre, budget of five)

- **fixture** — `frontmatter-absent`
- **invocation** — `/redline --genre=press-release --max=5 $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line naming the resolution and the stop, the corrected text, then two repaired findings and four unresolved.
- **side effects** — none.
- **criteria** —
  - `stop` — `pass` — the second of the three conditions, which no run in this record had reached: *two rounds spent, three unspent — the second round changed nothing, which stopped the loop*. The trace carries the proof rather than the claim: round 2's brief and the delivered text are the same text word for word, and the loop ended there with three rounds of a budget of five never spent.
  - `budget` — `pass` — a ceiling and not a quota, demonstrated at the size where the difference is visible: five available, two used.
  - `fresh` — `pass` — two subagents started fresh, each given the complete current text inline and the complete findings of the review immediately before it. Round 1 carried F1–F6; round 2 carried F1–F4, which is the re-review's list with the two repaired findings gone, not the corrector's report.
  - `verify` — `pass` — the findings that reached round 2 are a fresh review's, and the run's own account of the two repairs matches what the round-1 brief named.
  - `review` — `pass` — six findings, four of them the genre's own unfillable kind and two ordinary editorial ones.
  - `anti-slop` — `pass` — F5 is vague attribution — *fair rotas that nobody trusts* and *harder than any scheduling problem they have ever solved*, both quantified over teams in general with no source — and F6 is synonym cycling, one thing under *roster*, *the roster*, and *rota*. Both were repaired by cutting and by normalising the name, which is the catalogue's own repair for each.
  - `no-source` — `pass` — the unresolved findings say the genre's repair needs material the *text* does not contain, and the run closes by pointing at `--genre=article` rather than asking for a source. Nothing remarks that source verification was unavailable.
  - `mechanics` — `pass` — once, after the loop, and it found nothing.
  - `findings` — `pass` — four delivered with the artifact, marked unresolved, and named as one thing seen from four sides.
  - `sync` — `pass` — the fixture has no frontmatter and none was added.
  - `loading` — `pass` — `press-release.md` and `press-release.review.md`; no other genre resource was read.
  - `language` — `pass` — `en_GB` inferred and stated with its evidence, *artefact*, *rota*, British idiom.
  - `target` — `pass`. `effects` — `pass`. `leak` — `pass`.
- **unresolved findings** — four: no news anywhere, no printable fact, no close, and a text that argues rather than informs.
- **defects filed** — none.
- **notes** — the invocation is deliberate rather than a mistake, and it is the situation the third stopping condition needs. The press-release review guidance says four times over that a value the material does not carry is *reported rather than filled* — a missing contact, a vague fact, an absent quotation — and the correction brief forbids repairing a finding by inventing a fact. An essay held to that genre therefore produces a review whose remaining findings no corrector may touch, which is a correction that makes no relevant progress arriving on its own rather than being staged. The corpus supplies the material; only the invocation is new.

## `clean-en-GB` (press-release genre, budget of four)

- **fixture** — `clean-en-GB`
- **invocation** — `/redline --genre=press-release --max=4 $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected text, then four unresolved findings and a closing line saying which round stopped the loop.
- **side effects** — none.
- **criteria** —
  - `stop` — `pass` — the second condition again, independently: *the third changed nothing any finding named, which stopped the loop with one round of the budget unspent*. Round 3's brief carried F1–F4 and the delivered text is that brief's text unchanged.
  - `budget` — `pass` — four available, three used, one unspent.
  - `fresh` — `pass` — three subagents started fresh, each given the complete current text and the complete current findings. The lists move as a live review moves: F1–F6 in round 1, F1–F4 plus two findings the second review newly found in round 2, and F1–F4 alone in round 3.
  - `verify` — `pass` — round 2's brief carries two findings that were not in round 1's, which only a fresh review of the returned text could produce.
  - `review` — `pass`.
  - `anti-slop` — `pass` — the two findings repaired were vague attribution and over-strong assertion, both named as patterns and both repaired by deletion.
  - `no-source` — `pass` — each unresolved finding says the genre's repair would be fabrication from a text that carries no such fact, and the run closes by naming the genre as the thing to reconsider.
  - `mechanics` — `pass` — once, in `en_GB`, after the loop, and it found nothing.
  - `findings` — `pass` — four delivered, all unresolved.
  - `sync` — `pass` — the run states that no `kntnt` map is present and that none was added.
  - `loading` — `pass` — `press-release.md` and its review half only.
  - `language` — `pass` — `en_GB` inferred, and the British forms the fixture exists to protect survive the whole loop: *fortnight*, *judgement*, *summarise*, and no serial comma.
  - `target` — `pass`. `effects` — `pass`. `leak` — `pass`.
- **unresolved findings** — four.
- **defects filed** — none.
- **notes** — read this beside the `clean-en-GB` entry above, which changed nothing at all. The corpus supplies this fixture for a review *that should not be tempted into rewriting competent prose*, and the earlier run is where that is judged; this one holds the same prose to a genre it was not written in, which makes substantive change the correct outcome rather than a temptation. What the two entries say together is that the review's appetite tracks the contract it is given rather than the text's quality.

## `resembles-abt` (PAC selected, budget of five)

- **fixture** — `resembles-abt`
- **invocation** — `/redline --technique=pac --max=5 $RUN/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a resolution line, then the corrected text alone, with no findings section.
- **side effects** — none.
- **criteria** —
  - `stop` — `pass` — the first of the three conditions at a budget large enough for the difference to matter: *four of five corrections spent; the fifth went unspent because the final review found nothing left*. This is the entry that makes the two no-progress stops above readable as a stopping condition rather than as a budget quietly running out — the same size of budget, converging.
  - `budget` — `pass` — five available, four used, one unspent.
  - `fresh` — `pass` — four subagents started fresh, each with the complete current text and the complete findings of the review before it.
  - `verify` — `pass` — the finding lists shrink as a verified loop shrinks them, four to two to one, and round 4's single finding is one round 3's repair introduced rather than one it was given: round 3 was told the middle does not test the question, and round 4 was told the closing sentence's *the question* now points at two different questions.
  - `precedence` — `pass` — the technique came from the flag. The corpus rejects a technique *acted on when nothing selected it*; here something did, and the review is against PAC rather than against the ABT shape the text happens to fall into.
  - `review` — `pass`.
  - `no-source` — `pass`.
  - `mechanics` — `pass` — once, after the loop, and it found nothing.
  - `findings` — `pass` — none remained, and the artifact was delivered alone, which is what the contract asks for a clean run.
  - `sync` — `pass` — no map, none added.
  - `loading` — `pass` — `general.md`, `pac.md`, `pac.review.md`; no ABT resource was read.
  - `language` — `pass` — `en_GB` inferred.
  - `target` — `pass`. `effects` — `pass`. `leak` — `pass`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this run bears on #144 and narrows it. Four rounds on a 213-word text neither emptied it nor cut it back: every fact the fixture carries — 2016, nine requests a minute, four hundred, 90 milliseconds, two seconds, eleven days, 140 milliseconds, four days of arguing — survives all four rounds, and the text comes back slightly longer than it went in, with a premise sentence added at the front and a conclusion at the end. So a larger budget does not empty a text as such; what emptied `slop-heavy` was a review whose findings were nearly all *this claim has no support*, where the catalogue's own repair is deletion. #144 is about the interaction, not about the number.

## The correction brief's path, seen three more times

Three of these seven runs delegated corrections, and all three wrote the filled-in brief to `/tmp/redline-run/` — `brief.md` in one and `brief-1.md`, `brief-2.md`, `brief-3.md`, `brief-4.md` in the others. They were run one at a time with nothing else in flight, so nothing collided and none of the entries above is confounded. It is recorded because it is corroboration rather than a new observation: seven runs across two sessions have now independently invented the same fixed path under `/tmp`, which is what makes #143 a defect in the contract rather than an unlucky pair of runs. All three removed the directory when they were finished.

## Runs discarded

Four runs are named here so that the count of turns spent is honest, and they carry no criteria: what they say about this Skill is confounded by something that was not the Skill.

The evaluation staged each fixture in its own throwaway working copy and ran several at once. The working copies could not collide, and none did. The shared temporary directory could. Neither `SKILL.md` step 7 nor `correction.md` says how the filled-in correction brief reaches the subagent, so every run invented a mechanism, and four of them independently invented the same fixed path, `/tmp/redline-run/brief.md`. Two of those overlapped: one run wrote a 5,523-byte brief holding two findings, dispatched its subagent, and had the file and its directory deleted underneath it, while the subagent read a 6,774-byte brief holding three differently worded findings against an unrelated text.

Both runs that met it recovered and said so unprompted, which is worth recording: one subagent noticed that the text in the brief was not the text it had been sent to repair and repaired the right one, and its main run verified the returned text by diffing against the real artifact on disk rather than against anything under `/tmp`; the other moved to a private directory and rebuilt from the text and findings it was still holding. Both delivered results answerable to the real artifact. They are discarded anyway, because *it recovered* is not what a record should have to say about a correction round, and because the recovery depended on a subagent happening to check.

The four fixtures — `flawed-sv`, `new-file`, `existing-file`, and `slop-heavy` at `--max=3` — were re-run one at a time with nothing else in flight, and it is those re-runs the entries above record. Three of them came back materially different from their discarded attempt, which is the ordinary variance of a review rather than an effect of the collision: `flawed-sv` and `existing-file` each found no substantive defect the second time where the first had found one or two, and `new-file` resolved both of its findings where the first attempt had carried one forward. The underlying behaviour — an unspecified handover through a predictable shared path — is #143.

One further run is named for completeness and is not discarded for any reason of its own. The `--max=-1` refusal was made once before the harness was changed to record each run's full tool trace rather than its reply alone, and was then made again under the new recording. Both produced the same refusal; it is the second that the entry above records.
