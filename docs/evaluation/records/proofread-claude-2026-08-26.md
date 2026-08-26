# proofread — claude — 2026-08-26

- **record** — `proofread-claude-2026-08-26`
- **date** — `2026-08-26`
- **ticket** — `#156`
- **skill** — `proofread`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.246
- **corpus commit** — `46ba9c1`

## Run conditions

The Skill was run as a user of it runs it, in Claude Code, against the Skill as installed at `~/.claude/skills/proofread`. `diff -r` reported that directory byte-identical to `skills/editorial/proofread/` at the corpus commit, and the same for `~/.claude/skills/kntnt/` against `skills/kntnt/` — the Manager and the Collection Library the Skill resolves its language resources and its delivery contract from — with no difference but the untracked `__pycache__` directories the repository working tree carries and an installed copy does not. Proofread declares no peer Skill, so the Manager and its Library are the whole of its dependencies.

Each fixture ran in a Claude Code agent session of its own, started from this session, with no memory of any other run and no access to this repository's evaluation material: the turn carried the invocation and nothing else, and no run was given the Skill's own instructions, the ticket, or the criteria below. Each ran in its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says — `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form.

**side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself. Where a run delivered to a file, the file on disk is what was judged; where it delivered to the response, the reply is.

Three conditions of this machine and this method are worth a later reader's attention.

- **`/proofread` is ambiguous here.** A legacy plugin, `kntnt-text-skills:proofread` (version 0.10.0), is installed beside the Collection's Skill and answers to the same bare name, exactly as the previous Claude record for this Skill describes. Every by-name run below therefore carried one added routing sentence — that two Skills answer to `proofread` here, that the user means the Skill named exactly `proofread`, and that the plugin is not it. The sentence names which Skill to start and says nothing about what to do once it starts.
- **Model invocation was tested without that sentence**, since a routing hint would decide the very thing those runs exist to observe. Those runs were asked to name which Skill they started, and their entries record it.
- **A response-only delivery cannot be checked byte for byte.** The transport that carries a sub-session's reply back HTML-escapes some characters, so `&` arrives as `&amp;`. That is an artifact of the harness and not of the Skill, and it is why the two code-carrying fixtures were additionally run to a file: `156-45` and `156-46` are the entries whose code fidelity is checked against bytes on disk rather than against a transcript.

Judging was done from the delivered reply and the filesystem inventory alone, against the criteria below, fixture by fixture, before any GPT-family record existed to compare with. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

The criterion identifiers are stable across entries: `trigger` (the Skill started, or did not, as the description bounds it), `language` (the resolved language is the one the precedence names), `mechanics` (the mechanical layer is corrected), `preserve` (everything else comes through untouched, valid alternatives included), `code` (a code sample produces no finding and comes back byte for byte), `no-drift` (no stylistic improvement), `status` (the short no-change status where the contract asks for one), `target` (the artifact went where the output contract sends it), `effects` (the filesystem shows what the contract allows and nothing else), `refusal` (a refused invocation names the problem, prints the synopsis, and leaves nothing behind).

## `flawed-en-US`

- **fixture** — `flawed-en-US`
- **invocation** — `/proofread $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete corrected text came back in the response, followed by a list of fourteen corrections and a note of the two things left alone as valid choices; nothing was written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — resolved `en_US` by inference from the text's own `normalize` and `catalog`, with no flag, no frontmatter, and no instruction in play.
  - `mechanics` — `pass` — `writen`, `writting`, `It's job`, `Its that`, `into into`, `wasnt`, `dont`, `isnt`, `doesnt`, `would of been`, `The bug were`, `differences was`, `for four year`, and the US placement of the full stop inside `"rewrite things."` were all corrected.
  - `preserve` — `pass` — the American spellings, the heading, the paragraphing, the hedges, and the closing opinion are unchanged; the diff against the fixture touches nothing but the errors.
  - `no-drift` — `pass` — no sentence was restructured and nothing was tightened, in a text whose third paragraph invites both.
  - `target` — `pass` — no destination was named and the response received the artifact.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the two clause joints the fixture stages in opposite directions were both settled correctly: the comma in *The bug was not in the parsing at all, it was in a silent retry* stands, named in the reply as the negative-positive contrast the shared mechanics contract protects; the unrelated pair in *We finished in March, the finance team got a new reporting tool the same month* was corrected at the joint with a period, with no conjunction supplied and neither clause moved. The spaced em dashes were left, which `156-27` did not do; see that entry.

## `flawed-en-US` (In-place Editing)

- **fixture** — `flawed-en-US`
- **invocation** — `/proofread --in-place $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place
- **observed delivery** — the reply reported the file replaced and listed the corrections grouped by kind; the corrected text was not repeated in full.
- **side effects** — `corpus/prose/flawed-en-US.md` replaced. Nothing else created, replaced, or removed.
- **criteria** —
  - `mechanics` — `pass` — `diff` against the fixture shows the same fourteen corrections on disk.
  - `preserve` — `pass` — the diff is four changed lines and touches nothing but the errors; wording, structure, hedges, and the closing opinion are as they were.
  - `no-drift` — `pass` — nothing in the replaced file is an improvement rather than a correction.
  - `target` — `pass` — the source file itself received the result, and no copy was left beside it.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the negative-positive comma is untouched here too, correctly, and named in the reply for the same reason.

## `flawed-sv`

- **fixture** — `flawed-sv`
- **invocation** — `/proofread $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete corrected text came back in the response with a Swedish list of six corrections; nothing was written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — Swedish was inferred from the text and the whole reply was written in it, with no English anywhere in the exchange.
  - `mechanics` — `pass` — every planted error was corrected: `det det`, `dem svåra` → `de svåra`, `uptäckte` → `upptäckte`, the split compound `avgångs samtal` → `avgångssamtal`, and the missing word in `vi tänker inte gå tillbaka`; the inflection `Antalet ärende` → `ärenden` was corrected with them.
  - `preserve` — `pass` — `hen` stands, which the fixture names as the trap: it is a valid Swedish pronoun and not an error.
  - `no-drift` — `pass` — the argument, the paragraph order, and the numbers are as they were.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the fixture that shows mechanical correction is language-specific in practice and not only in the contract; it is, and the report about the text is in the text's language as the delivery contract requires.

## `clean-en-GB`

- **fixture** — `clean-en-GB`
- **invocation** — `/proofread $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a two-sentence status saying no mechanical errors were found and that nothing was written; the text was not repeated.
- **side effects** — none.
- **criteria** —
  - `status` — `pass` — the short no-change status came back instead of the text, which is what the contract asks of a response-targeted run that corrected nothing.
  - `preserve` — `pass` — `judgement`, `summarise`, `towards`, `fortnight`, and the absent serial comma all stand.
  - `no-drift` — `pass` — competent prose came back unedited, and the reply proposed no improvements.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `clean-en-GB` (unchanged result, explicit different file)

- **fixture** — `clean-en-GB`
- **invocation** — `/proofread --output=$RUN/out/clean-copy.md $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/clean-copy.md`
- **observed delivery** — the reply said no mechanical errors were found, named the two British forms and the unspaced em dash it had left, and said the complete text had been written to the named path anyway because an explicit different destination was chosen.
- **side effects** — `out/clean-copy.md` created. The source is untouched.
- **criteria** —
  - `status` — `pass` — the no-change status did not suppress the artifact, which is the distinction the contract draws between a response target and a named one.
  - `target` — `pass` — the file was created at exactly the named path, and `diff` against the source reports no difference.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `slop-heavy`

- **fixture** — `slop-heavy`
- **invocation** — `/proofread $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a short status: no mechanical errors found, nothing written.
- **side effects** — none.
- **criteria** —
  - `status` — `pass` — a text with nothing mechanically wrong with it produced the status rather than a repeated text.
  - `preserve` — `pass` — the empty opening, the false contrasts, the vague attribution, and the rhetorical-question close all stand; none of them is a mechanical error and none was touched.
  - `no-drift` — `pass` — the fixture most likely to tempt a pass into improving prose produced no edit at all.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the boundary the Skill exists to hold: the patterns are an anti-slop pass's business, and this Skill loaded no anti-slop catalogue and acted on none of them.

## `slop-heavy-sv` (language inferred)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/proofread $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back in the response with a Swedish list of three corrections, all of them punctuation.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — Swedish was inferred and the whole reply is in Swedish.
  - `mechanics` — `pass` — the curly English quotation marks around `kundresa` were replaced with the Swedish `”…”` pair, which the `sv` mechanics scope names; the comma in `Dessutom, är det viktigt` and the serial comma in `teknik, processer, och kultur` were removed.
  - `preserve` — `pass` — every slop pattern in a text built out of them is still there: the metaphor stock, the superlatives, the triads, the empty attribution, the openings and closings.
  - `no-drift` — `pass` — not a word of the prose was rewritten.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — see the note.
- **notes** — of the three corrections, only the quotation marks are named in the `sv` resource's **Mechanics** section. The comma after a fronted connective adverb and the serial comma inside a Swedish list are named only in its **Anti-slop** section, which this Skill's step 6 forbids it to load. Both are genuine Swedish punctuation errors and correcting them is inside the Skill's stated contract, so no criterion fails on them — but a rule a mechanical pass has to apply, written only where a mechanical pass may not look, is why runs disagree about it. The next entry, run over the same fixture with the language named, corrected the serial comma nowhere; `156-10` and `156-11` corrected an em dash this run left. Filed as #167.

## `slop-heavy-sv` (language named explicitly)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/proofread --language=sv $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back in the response with a Swedish list of two corrections.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `--language=sv` settled the parameter and the reply is in Swedish.
  - `mechanics` — `pass` — the quotation marks and the comma after `Dessutom` were corrected.
  - `preserve` — `pass` — the patterns, the em dashes, and the `&` all stand, and the reply says explicitly that neither the `sv` scope nor the shared contract names them as errors.
  - `no-drift` — `pass` — nothing was rewritten.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #167.
- **notes** — this run left the serial comma the previous one removed. The two runs differ on exactly the item the `sv` resource files under Anti-slop rather than under Mechanics, which is the evidence #167 rests on.

## `code-carrying` (response)

- **fixture** — `code-carrying`
- **invocation** — `/proofread $RUN/corpus/prose/code-carrying.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back in a fenced block with three corrections named, all of them in the prose.
- **side effects** — none.
- **criteria** —
  - `mechanics` — `pass` — the article's own three errors were corrected: `Its` → `It's`, `enable` → `enables`, and the duplicated `can can`.
  - `preserve` — `pass` — the patterns in the article's sentences are untouched, which is what a mechanical pass owes an anti-slop pass's material.
  - `code` — `pass` — `recieved` in the thrown message, `seperate` in the indented block's comment, the docstring's and the comments' patterns, both identifiers named after patterns, and the two inline spans `not_just_about.ttl` and `recieved_at` all came back as they were, and no finding was located inside a sample.
  - `no-drift` — `pass` — nothing was improved.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — `code` is judged here from the reply. `156-45` runs the same fixture to a file and checks the same claim against bytes on disk.

## `code-carrying-sv` (language inferred)

- **fixture** — `code-carrying-sv`
- **invocation** — `/proofread $RUN/corpus/prose/code-carrying-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back in the response with a Swedish list of six corrections and an explicit statement of what inside the code was left alone.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — Swedish was inferred and the reply is in Swedish.
  - `mechanics` — `pass` — the article's own four errors were corrected: `dem svåra` → `de svåra`, `uptäckte` → `upptäckte`, the split compound `drift instruktion` → `driftinstruktion`, and the duplicated `om om`.
  - `preserve` — `pass` — the Swedish patterns in the article's sentences are untouched.
  - `code` — `pass` — the reply names `emmot`, `seperat`, `uppdaterings loop` and the inline spans as quoted material and leaves them; no finding is located inside a sample.
  - `no-drift` — `pass` — nothing was rewritten.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #167.
- **notes** — two of the six corrections are the Anti-slop-only items #167 is about: the comma in `Dessutom, blir` and the unspaced em dash in `snabbt—det`, changed here to the spaced en dash. The em dash is not named in the `sv` **Mechanics** section at all, and the two `slop-heavy-sv` runs above left the same construction alone. `code` is judged here from the reply; `156-46` checks it against bytes on disk.

## `code-carrying-sv` (language named explicitly)

- **fixture** — `code-carrying-sv`
- **invocation** — `/proofread --language=sv $RUN/corpus/prose/code-carrying-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back with the same six corrections and the same explicit list of untouched code.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `--language=sv` settled the parameter.
  - `mechanics` — `pass` — the same four planted errors were corrected.
  - `preserve` — `pass` — the patterns in the prose stand.
  - `code` — `pass` — the same code items are named as quoted material and left.
  - `no-drift` — `pass` — nothing was rewritten.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #167.
- **notes** — naming the language changed nothing here, which is the point of running the fixture both ways.

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/proofread $RUN/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a two-sentence status: no mechanical errors, nothing changed, nothing written.
- **side effects** — none.
- **criteria** —
  - `status` — `pass` — the no-change status rather than a repeated text.
  - `preserve` — `pass` — the text is untouched, the *Therefore* opening its third paragraph included.
  - `no-drift` — `pass` — competent prose came back unedited.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — no technique was reported, recorded, or acted on, which is the fixture's whole question. Proofread resolves no technique at all, so it passes this fixture by construction rather than by judgement.

## `mixed-language`

- **fixture** — `mixed-language`
- **invocation** — `/proofread $RUN/corpus/prose/mixed-language.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one question and nothing else: the reply quoted a sentence showing the alternation, said that which language it applies changes what counts as an error, and asked whether to proofread in Swedish or in English and which English. It stated that nothing had been read against any rule set and nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — no language was picked and acted on; the material the corpus built to defeat inference produced the question the contract asks for.
  - `effects` — `pass` — the inventory is identical before and after, so the question cost nothing to leave unanswered.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run also offered to run the pass twice, once per language. That is an offer rather than an action and nothing was done on it.

## `locale-divergent` (en_GB)

- **fixture** — `locale-divergent`
- **invocation** — `/proofread --language=en_GB $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status listing the British forms it had checked and left.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `--language=en_GB` settled the parameter.
  - `status` — `pass` — the short status rather than a repeated text.
  - `preserve` — `pass` — `organised`, `specialised`, `cancelling`, `judgement`, `licence` as the noun against `licensed` as the verb, `£14,500`, and the full stop outside the closing quotation mark all stand; the fixture's British forms were not treated as errors under the British locale.
  - `mechanics` — `pass` — the numeric date `3/4` is well-formed British and was left alone.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `locale-divergent` (en_US)

- **fixture** — `locale-divergent`
- **invocation** — `/proofread --language=en_US $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back with the American forms applied, followed by a paragraph saying that one correction rested on a reading the user should confirm.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `--language=en_US` settled the parameter.
  - `mechanics` — `pass` — `organised` → `organized`, `specialised` → `specialized`, `judgement` → `judgment`, `cancelling` → `canceling`, `licence` → `license` twice, and the full stop moved inside the closing quotation mark are all the resolved locale's own conventions.
  - `preserve` — `fail` — **an unsupported fact.** The source's `3/4` was rewritten as `4/3`, on the run's own stated assumption that the source had been written in British day-month order. Nothing in the material says which order it is in; the fixture supplies the date precisely because it is ambiguous, and the corpus names this rewriting as a rejection. The reply's own hedge — *one correction rests on a reading you should confirm* — is the run saying it had asserted something the text does not carry.
  - `no-drift` — `pass` — nothing else about the note was rewritten; `autumn`, `£14,500`, and `has got harder` were named and left.
  - `effects` — `pass` — the inventory is identical before and after, so the failure is in the delivered text and not on disk.
- **unresolved findings** — the date reading, reported with the artifact.
- **defects filed** — #166.
- **notes** — the contextual-instruction run below resolves the same locale from the same file and leaves the date alone, saying explicitly that reordering it would change what the note claims rather than how it is written. Neither the `en_US` mechanics scope nor the shared mechanics contract says that an ambiguous numeric date is outside a mechanical pass's reach, and two runs of one Skill at one locale disagreed about it. The defect was already open when this record was written: #166, filed from the opposite family's run of the same fixture under `en_GB`, where the same date was expanded to `3 April` instead. This run is a second, independent instance of it under the other locale, and #166's acceptance criteria already name both.

## `locale-divergent` (contextual instruction)

- **fixture** — `locale-divergent`
- **invocation** — `/proofread $RUN/corpus/prose/locale-divergent.md -- Treat this as American English.`
- **contextual instruction** — `Treat this as American English.`
- **output target** — `response`
- **observed delivery** — the complete text came back with seven corrections named, followed by a paragraph explaining why the numeric date was left as it stands.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — no flag and no frontmatter, so the Contextual Instruction is the level that answered, which is the third step of the precedence and the one this fixture stages.
  - `mechanics` — `pass` — the same American spellings, the noun-verb collapse, and the quotation placement were applied.
  - `preserve` — `pass` — `3/4` stands, and the reply says why: the string is well-formed under either locale, and reordering it would change what the note claims rather than how it is written.
  - `no-drift` — `pass` — `autumn`, `has got harder`, and `£14,500` were named and left.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — the date's ambiguity, reported with the artifact as something for the user's eye rather than acted on.
- **defects filed** — #166.
- **notes** — this is the correct handling of the same material the entry above got wrong, from the same resolved locale.

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/proofread $RUN/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status, with one sentence naming `en_GB` and saying it was taken from the `language` value in the document's own `kntnt` map.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the map answered, which is the second level of the precedence and the level this fixture stages; the code was reported in the normalized spelling the map carries.
  - `status` — `pass` — the short status rather than a repeated text.
  - `preserve` — `pass` — `60 per cent` and the rest of the British forms stand, and the frontmatter is untouched.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `handoff-present` (metadata against a contrary instruction)

- **fixture** — `handoff-present`
- **invocation** — `/proofread $RUN/corpus/frontmatter/handoff-present.md -- Use American English mechanics for this one.`
- **contextual instruction** — `Use American English mechanics for this one.`
- **output target** — `response`
- **observed delivery** — a no-change status, followed by a paragraph saying the language resolved to `en_GB` from the map, that the map sits above a Contextual Instruction in the precedence, and that the instruction was therefore suppressed rather than applied; it named `--language=en_US` as the gesture that would win.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the map beat the Contextual Instruction, which is the precedence working; the run continued rather than refusing the instruction as unaddressable.
  - `status` — `pass` — the short status came back, and the suppressed instruction was named beside the resolved configuration exactly as the Invocation Envelope says it should be.
  - `preserve` — `pass` — nothing was changed, and no American form was applied.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the clearest single demonstration in the record that suppression is treated as precedence rather than as an error.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/proofread --language=sv $RUN/corpus/frontmatter/handoff-conflicting.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status written in Swedish, saying that the frontmatter declares `kntnt.language: en_US`, that the flag takes precedence, and that the frontmatter was left untouched.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the explicit value beat the map, which is the top of the precedence; the reply is in the artifact's language, not the invocation's.
  - `status` — `pass` — the short status in Swedish rather than a repeated text.
  - `preserve` — `pass` — the frontmatter is byte-identical, contradiction and all.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's rejection about a delivered file carrying a map that contradicts the resolved configuration does not reach this Skill: Proofread never writes a `kntnt` map and never edits frontmatter, so a contradiction it was not asked to resolve is left where it is. Genre is not a parameter this Skill has, so the half of the fixture that turns on genre is not exercised here.

## `handoff-partial`

- **fixture** — `handoff-partial`
- **invocation** — `/proofread $RUN/corpus/frontmatter/handoff-partial.md -- The language is Swedish.`
- **contextual instruction** — `The language is Swedish.`
- **output target** — `response`
- **observed delivery** — a no-change status in Swedish, saying that the language came from the instruction because the `kntnt` map carries only `technique` and no `language`, that the Swedish passages were read against Swedish mechanics and carry no errors, and that the English passages are a wording choice rather than an error and were left alone. It named one borderline it had deliberately left: `for` in *gör störst skillnad for the people who actually read it*, read as the English preposition at the language switch rather than as a misspelled *för*.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the map's absent `language` key fell through to the Contextual Instruction, which settled it; no language question was asked where the instruction had already named one.
  - `preserve` — `pass` — nothing was changed; the English passages were not translated and the frontmatter is untouched.
  - `status` — `pass` — the short status in the artifact's resolved language.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — the `for`/`för` borderline, reported with the status.
- **defects filed** — none.
- **notes** — the two absent keys were not read as a reason to stop, to ask for a complete map, or to treat the map as unusable, which is what the fixture is built to catch. Proofread resolves no technique, so the map's one key was never consulted — the per-field resolution this fixture stages across three parameters is only partly reachable through this Skill, and the language half of it is what this entry establishes.

## `handoff-unusable` (nothing suppresses the map)

- **fixture** — `handoff-unusable`
- **invocation** — `/proofread $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a refusal headed *Unusable artifact metadata*: it quoted the map, named `en_UK` as neither a canonical code nor an installed alias, listed the three installed resources, said explicitly that it would not read the value as the code it resembles, and offered the two ways forward.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `en_UK` was not quietly read as `en_GB`, and the run did not continue as though the metadata had been usable.
  - `refusal` — `pass` — the problem is named and nothing was corrected or written.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this refusal names the problem and points at the two gestures rather than printing the synopsis, which is what the Skill's step 5 asks for: it is an unusable-metadata report rather than a syntax refusal, and the syntax refusals below do print the synopsis.

## `handoff-unusable` (a flag supersedes the map)

- **fixture** — `handoff-unusable`
- **invocation** — `/proofread --language=en_GB $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status, saying that the document's `kntnt.language` is `en_UK`, that the explicit option settled the language, and that the field was therefore left alone and did not stop the run.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — a `--language` value settles the parameter and suppresses the unusable-metadata stop, which is exactly what the Skill's step 5 says.
  - `status` — `pass` — the short status rather than a repeated text.
  - `preserve` — `pass` — the unusable map is still in the file, unedited.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the two `handoff-unusable` runs together are what shows the stop is conditional on precedence rather than on the metadata alone.

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/proofread $RUN/corpus/frontmatter/frontmatter-unrelated.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status, naming `en_GB` as inferred from the text itself and saying that with no `kntnt` map present, `lang: fr`, `language: Esperanto`, `genre`, and `technique` are the document's own fields rather than configuration.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — none of the four bait keys was read as configuration, and inference reached the language of the text.
  - `preserve` — `pass` — the frontmatter block is untouched, bait keys included.
  - `status` — `pass` — the short status rather than a repeated text.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run named all four bait keys explicitly, so this is a decision it made rather than one it happened not to reach.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/proofread $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status, saying the file carries no frontmatter and so no language metadata, and that the language fell through to inference.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — inference answered where nothing above it did.
  - `status` — `pass` — the short status rather than a repeated text.
  - `preserve` — `pass` — no `kntnt` map was added to a file that had no frontmatter at all.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — no metadata was demanded and nothing was refused, which is the baseline this fixture exists to establish.

## `response-default`

- **fixture** — `response-default`
- **invocation** — `/proofread $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status; the reply named the clause series in the first paragraph as a coordinated series rather than a splice, and said nothing was written to disk.
- **side effects** — none.
- **criteria** —
  - `target` — `pass` — no destination was named, so nothing left the response.
  - `effects` — `pass` — no file was created, replaced, or removed anywhere under the working copy.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the source here is a local file, and supplying one selected no destination, which is the half of the default the corpus is testing.

## `response-default` (the value stated explicitly)

- **fixture** — `response-default`
- **invocation** — `/proofread --output=response $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete corrected Swedish text in the response, with the corrections listed in Swedish.
- **side effects** — none.
- **criteria** —
  - `target` — `pass` — `--output=response` states the default rather than naming a file, and the artifact stayed in the response.
  - `mechanics` — `pass` — the same six corrections as the bare run over this fixture.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — no corpus fixture stages this; it is here because the help page says the value `response` states the default explicitly, and a flag that is accepted and does nothing would be the thing the Skill's own diagnostics warn against.

## `new-file`

- **fixture** — `new-file`
- **invocation** — `/proofread --output=$RUN/out/draft.md $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/draft.md`
- **observed delivery** — the reply named the path written and listed sixteen corrections; the text was not repeated.
- **side effects** — `out/draft.md` created. The source is untouched.
- **criteria** —
  - `target` — `pass` — exactly that one file was created, nothing was made to hold it, and the artifact did not also appear in the response.
  - `mechanics` — `pass` — the fourteen errors the other runs over this fixture corrected are corrected on disk.
  - `effects` — `pass` — one file created and nothing else touched; no partial file was left behind.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this run additionally closed up the two spaced em dashes to the unspaced American form, which the `en_US` resource's **Mechanics** section names as the convention (*Em dashes are set unspaced*). Three other runs over the same fixture left them, calling them an established variant used consistently. Both readings are defensible on the resource as written — it states the convention without saying whether the spaced form is an error — so no criterion fails either way, and the divergence is recorded in #167 with the Swedish cases.

## `existing-file`

- **fixture** — `existing-file`
- **invocation** — `/proofread --output=$RUN/corpus/output/existing-target.md $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — the reply said the file already existed and had been overwritten, and listed the corrections; the text was not repeated.
- **side effects** — `corpus/output/existing-target.md` replaced. Nothing else created, replaced, or removed.
- **criteria** —
  - `target` — `pass` — the occupant was replaced, no sibling was written beside it, and no second confirming gesture was demanded; the file on disk is byte-identical to the in-place run's corrected text for the same fixture.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — naming the exact existing path was taken as the authorisation, which is what the corpus asks.

## `existing-directory`

- **fixture** — `existing-directory`
- **invocation** — `/proofread --output=$RUN/out $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — a Swedish reply naming the derived filename and listing the six corrections; the text was not repeated.
- **side effects** — `out/flawed-sv.md` created. The source is untouched.
- **criteria** —
  - `target` — `pass` — the name was derived from the source's basename rather than from the directory, kept the source's `.md` extension, and landed inside the named directory.
  - `mechanics` — `pass` — the corrected text is on disk, not the source's.
  - `effects` — `pass` — one file created, nothing written outside the directory.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the report about the text is in Swedish, which is the delivery contract's rule about the language of a report rather than of an invocation.

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/proofread --output=$RUN/corpus/output/collision $RUN/corpus/output/interview-notes.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the reply said the text had needed no correction, that a directory destination receives the artifact anyway, and named the file written.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants are unchanged.
- **criteria** —
  - `target` — `pass` — the stem stayed `interview-notes` and the first free candidate in ascending order was taken; nothing was built by suffixing the colliding candidate.
  - `status` — `pass` — the no-change status did not suppress a directory delivery.
  - `effects` — `pass` — one file created, neither occupant overwritten.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — `interview-notes-2-2.md`, the name the corpus names as the wrong answer, was not written.

## `read-only-source`

- **fixture** — `read-only-source`
- **invocation** — `/proofread --in-place $RUN/corpus/output/readonly-source.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place, refused
- **observed delivery** — a refusal naming the file as read-only and In-place Editing as requiring a writable local source, followed by the synopsis and a pointer to `/proofread --help`.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named, the synopsis is printed, and the run stopped.
  - `effects` — `pass` — the inventory is identical before and after, `out/` is empty, and the file is still mode `-r--r--r--`: no permission was changed to make the write possible and no result was written elsewhere as a silent substitute.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run reported using `test -w` to establish the condition by reading, which is what the delivery contract asks for so that a refusal has nothing written behind it.

## `in-place-request`

- **fixture** — `in-place-request`
- **invocation** — `/proofread --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place
- **observed delivery** — a no-change status naming the file and saying it was left unchanged.
- **side effects** — none.
- **criteria** —
  - `status` — `pass` — an in-place run that found nothing to change wrote nothing, which is what the contract asks; the file's timestamp does not claim that something happened.
  - `effects` — `pass` — the inventory is identical before and after, and no copy was left beside the source.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the fixture's own rejection — *a rewritten file where the run found nothing to change and a short status was the contract* — is the one this entry turns on, and it did not happen.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/proofread --output=$RUN/corpus/output/in-place-source.md $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying `--output` names the input file's own path and that this is refused in favour of `--in-place`, quoting the in-place invocation to use, followed by the synopsis and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named, the refusal points at In-place Editing as the recognisable authorisation, and the synopsis is printed.
  - `effects` — `pass` — the file was not replaced and the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/proofread --output=$RUN/out/copy.md --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying the invocation names two destinations for one text, followed by the synopsis and the help pointer, and stating that nothing was read, corrected, or written.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named and the synopsis printed.
  - `effects` — `pass` — neither half was executed: `out/copy.md` does not exist and the source is unchanged.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `url-source` (In-place Editing refused)

- **fixture** — `url-source`
- **invocation** — `/proofread --in-place https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying `--in-place` requires one writable local file and that a URL is not one, that fetching one grants no right to write anything back, followed by the synopsis, the help pointer, and two suggested alternatives.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named and the synopsis printed; nothing was fetched.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the refusal was made by reading the invocation, before the network was touched at all.

## `url-source` (URL read, filename derived from it)

- **fixture** — `url-source`
- **invocation** — `/proofread --output=$RUN/out https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the derived path and listed eight mechanical corrections in the RFC's prose, with a paragraph on what it had left as preference rather than error; the text was not repeated.
- **side effects** — `out/rfc2119.txt` created. Nothing else.
- **criteria** —
  - `target` — `pass` — the filename was derived from the URL rather than from any source basename, and carries the extension matching the fetched text's format.
  - `preserve` — `pass` — the RFC's own 72-column wrapping, page furniture, form feeds, running heads, and the double space inside the quoted boilerplate were named and left; the corrections are agreement, a missing comma, a period placement, and one misspelling.
  - `effects` — `pass` — one file created inside the named directory, nothing outside it.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the one fixture whose material arrives over the network, and it is the only run in the record that depended on anything outside the working copy.

## `code-carrying` (delivered to a file, code checked on disk)

- **fixture** — `code-carrying`
- **invocation** — `/proofread --output=$RUN/out/kill-switches.md $RUN/corpus/prose/code-carrying.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/kill-switches.md`
- **observed delivery** — the reply named the path and listed three corrections, all in the prose, and named the code items it had left as quoted material.
- **side effects** — `out/kill-switches.md` created. The source is untouched.
- **criteria** —
  - `mechanics` — `pass` — `Its` → `It's`, `enable` → `enables`, and the duplicated `can can` are corrected on disk.
  - `code` — `pass` — `diff` against the fixture reports exactly two changed lines, both of them prose; the fenced JavaScript block and the indented block hash identically to the fixture's, and both inline spans are still there. `recieved`, `recieved_at`, and `seperate` are uncorrected, and no identifier was renamed.
  - `preserve` — `pass` — the two changed lines differ only at the three errors, and the article's own patterns are untouched.
  - `target` — `pass` — the file was created at the named path and the text was not repeated in the response.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the entry that checks the code claim against bytes rather than against a transcript, which the response-targeted run over the same fixture could not do.

## `code-carrying-sv` (delivered to a file, code checked on disk)

- **fixture** — `code-carrying-sv`
- **invocation** — `/proofread --output=$RUN/out/avstangningsknappen.md $RUN/corpus/prose/code-carrying-sv.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/avstangningsknappen.md`
- **observed delivery** — a Swedish reply naming the path and six corrections, with an explicit paragraph on what inside the code was left and why.
- **side effects** — `out/avstangningsknappen.md` created. The source is untouched.
- **criteria** —
  - `language` — `pass` — Swedish was inferred and the report is in Swedish.
  - `mechanics` — `pass` — the four planted prose errors are corrected on disk.
  - `code` — `pass` — `diff` against the fixture reports exactly three changed lines, all of them prose; the fenced Python block and the indented block are byte-identical, `emmot` and `seperat uppdaterings loop` are uncorrected, and the inline spans `nyckeln_till_framgang.ttl` and `emmottagen_tid` are unedited.
  - `preserve` — `pass` — `Drift & utveckling` is on disk with its literal ampersand, which settles that the `&amp;` seen in the response-targeted runs was the transport and not the Skill.
  - `target` — `pass` — the file was created at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — none.
- **defects filed** — #167.
- **notes** — two of the three changed lines carry the Anti-slop-only items #167 is about, the em dash among them.

## `<undeclared flag>`

- **fixture** — none; no corpus fixture stages an invalid form, and the Skill's DIAGNOSTICS section names several.
- **invocation** — `/proofread --force $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming `--force` as unrecognized and listing the three options the Skill takes, followed by the synopsis, the help pointer, and two suggested corrected invocations.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the flag was refused rather than ignored, which is what the Skill's own diagnostics say a flag with no work to do gets.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `<two Text Artifacts>`

- **fixture** — none; a variant of the same DIAGNOSTICS list.
- **invocation** — `/proofread $RUN/corpus/prose/flawed-en-US.md $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal saying the invocation names two texts where the Skill processes one, that the language and destination cannot then be settled once for one text, followed by the synopsis and the two separate invocations to run instead.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named and the synopsis printed.
  - `effects` — `pass` — neither file was read against the rules and nothing was written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the two paths are in two different languages, so a Skill that had resolved them into a configuration per file would have been visible in the reply; it did not.

## `<Text Artifact before a flag>`

- **fixture** — none; a variant of the same DIAGNOSTICS list.
- **invocation** — `/proofread $RUN/corpus/prose/flawed-en-US.md --language=en_US`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming the out-of-order form — the path written before a flag rather than after every flag — followed by the synopsis, the help pointer, and the corrected invocation.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named and the synopsis printed.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the invocation is unambiguous to a reader and was still refused rather than repaired, which is the behaviour the DIAGNOSTICS section describes.

## `flawed-en-US` (model invocation, proofreading term)

- **fixture** — `flawed-en-US`
- **invocation** — `Can you proofread $RUN/corpus/prose/flawed-en-US.md for me?`
- **contextual instruction** — `none`; this run carried no routing sentence, since a routing hint would decide what the run exists to observe.
- **output target** — `response`
- **observed delivery** — the run reported starting `proofread`, and returned the complete corrected text in the response with twelve corrections listed paragraph by paragraph and three things named as deliberately left.
- **side effects** — none.
- **criteria** —
  - `trigger` — `pass` — the request uses a proofreading term and names a specific text, and the Skill started; the reply names loading the shared mechanics contract and the US mechanics scope, so it is the Skill that ran and not a general edit.
  - `mechanics` — `pass` — the same set of corrections as the by-name runs over this fixture.
  - `preserve` — `pass` — the negative-positive comma, the American spellings, and the spaced em dashes were named and left.
  - `target` — `pass` — nothing was named as a destination and the artifact stayed in the response.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the Skill answered to the bare name here without the routing sentence the by-name runs carried, which is worth noting given the plugin collision described under **Run conditions**: the collision is a `/proofread` routing problem rather than a model-invocation one.

## `flawed-en-US` (model invocation, mechanical-only request)

- **fixture** — `flawed-en-US`
- **invocation** — `Fix the spelling and grammar mistakes in $RUN/corpus/prose/flawed-en-US.md — nothing else, just the language errors.`
- **contextual instruction** — `none`; no routing sentence.
- **output target** — the source file, in place — which is the finding below.
- **observed delivery** — the run reported starting `proofread`, said it had corrected the file in place, and listed the corrections by kind.
- **side effects** — `corpus/prose/flawed-en-US.md` replaced. The file on disk is byte-identical to the file the `new-file` run wrote from the same fixture.
- **criteria** —
  - `trigger` — `pass` — the request is unambiguously limited to mechanical language errors and names a specific text, and the Skill started.
  - `mechanics` — `pass` — the corrections on disk are the same mechanical set, with the American dash convention applied as in the `new-file` run.
  - `preserve` — `pass` — wording, meaning, tone, and structure are unchanged, and the negative-positive comma stands.
  - `target` — `fail` — **an incorrect side effect.** The source file was replaced although nothing in the turn chose a destination. The delivery contract makes the response the default and says that supplying a local file as source material selects no destination, and that persisting a result is the caller's explicit choice; *fix the mistakes in `<file>`* locates the mistakes rather than naming where the result goes. The model-invocation run over the same fixture in the entry above read an equivalent request as a response-targeted one.
  - `effects` — `fail` — the same finding read from the filesystem: exactly one file changed, and it is a file no destination named.
- **unresolved findings** — none.
- **defects filed** — #168.
- **notes** — the Skill's formal gesture for this is `--in-place`, and a model-invoked run has no flags to carry it. Nothing in the Skill or in the delivery contract says how a destination may be read out of natural language, so the two model-invocation runs above resolved the same question in opposite directions. #168 is filed on that gap rather than on this run: replacing a source on an ambiguous reading is the unsafe direction of an ambiguity, and it is the direction the contract's own reasoning argues against.

## `flawed-en-US` (model invocation withheld: improve)

- **fixture** — `flawed-en-US`
- **invocation** — `Please improve $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`; no routing sentence.
- **output target** — not applicable; the Skill did not start.
- **observed delivery** — the run reported starting no Skill, and said so explicitly: a general *improve* request is one the proofread Skill excludes. It then rewrote the file itself as an ordinary assistant task, cutting a sentence and rewording another.
- **side effects** — `corpus/prose/flawed-en-US.md` replaced — by the assistant, not by the Skill.
- **criteria** —
  - `trigger` — `pass` — the description's exclusion held: *improve* did not start the Skill.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the file was changed, and the change is not this Skill's: a Skill that did not run has no output contract to break. The entry records the side effect because the inventory shows it, and names whose it is. The rewrite it produced — a cut sentence, a tightened clause — is exactly the work the Skill refuses to do, which is why the exclusion is in its description.

## `flawed-en-US` (model invocation withheld: polish and tighten)

- **fixture** — `flawed-en-US`
- **invocation** — `Polish and tighten $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`; no routing sentence.
- **output target** — not applicable; the Skill did not start.
- **observed delivery** — the run reported starting no Skill when asked which it had started. It polished the file itself, reporting a word count from roughly 300 to 256 and a cut sentence, and flagged that the file's name and location suggested it might be a fixture meant to stay flawed.
- **side effects** — `corpus/prose/flawed-en-US.md` replaced — by the assistant, not by the Skill.
- **criteria** —
  - `trigger` — `pass` — *polish and tighten* did not start the Skill.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — a 300-to-256-word rewrite is the clearest illustration in the record of what the description's exclusions are protecting against.

## `flawed-en-US` (model invocation withheld: review and edit)

- **fixture** — `flawed-en-US`
- **invocation** — `Review and edit $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`; no routing sentence.
- **output target** — not applicable; the Skill did not start.
- **observed delivery** — the run reported starting no Skill, and edited the file itself: mechanical fixes, a comma splice repaired with a semicolon, and a cut sentence, with its reasoning given as editorial rather than mechanical.
- **side effects** — `corpus/prose/flawed-en-US.md` replaced — by the assistant, not by the Skill.
- **criteria** —
  - `trigger` — `pass` — *review and edit* did not start the Skill.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run's own justification for the cut is that the juxtaposition invites an unsupported causal inference. That is a review finding, which is Redline's business and not this Skill's, and it is the reason *review* is on the exclusion list.

## Fixtures deliberately skipped

Six fixtures were not run against this Skill. Each is recorded here rather than omitted, because a record silently missing a fixture reads later as a fixture that passed.

- `brief-short` — `skipped` — a brief for a draft. Proofread takes a Text Artifact to correct, not a brief to write from; the corpus's `Reject` line for it judges a draft's supported facts, which this Skill produces nothing to judge. Inline supply, the one thing it would additionally exercise, is not reachable through this Skill in a way the record does not already hold: the model-invocation runs above supply their text by path, and no fixture supplies an inline Text Artifact that a mechanical pass would treat differently from a file's contents.
- `brief-article-abt` — `skipped` — same reason; its rejections are about genre, technique, and attribution, none of which this Skill resolves.
- `brief-report-pac` — `skipped` — same reason.
- `brief-press-release-sv` — `skipped` — same reason. Swedish language inference, the part of it that could bear on this Skill, is exercised by `flawed-sv`, `slop-heavy-sv`, `code-carrying-sv`, `handoff-conflicting`, and `handoff-partial`.
- `interview-transcript` — `skipped` — its rejections concern quotation fidelity in a draft that quotes the speaker, which is Write's invariant. Proofreading a transcript would exercise nothing this record does not already hold.
- `factual-source-long` — `skipped` — its rejections concern causal claims and figures in a draft made from it, which this Skill neither makes nor can make.

`url-source` was run rather than skipped, in both the halves that reach this Skill: the In-place refusal and the filename derived from a URL. Its third half — a definition attributed to the RFC that the RFC does not give — belongs to a Skill that writes from the source, and this Skill wrote no such claim because it wrote no such text.

## What this record establishes, and what it does not

Forty-six fixture runs. Two of them carry a failing criterion; the other forty-four are clean throughout.

The first failure is `locale-divergent` under `--language=en_US`, where an ambiguous numeric date was reordered on an assumption about the source's own locale. It is a second instance of a defect the opposite family's run had already opened as #166, from the same fixture under the other locale. Two further defects were filed from this run: #167, on Swedish punctuation rules that a mechanical pass must apply being written only in the scope it may not load, which is the root cause under the already-filed #163 and #165; and #168, on a model-invoked run having no rule for its Output Target, which replaced a source no destination had named.

What holds up without qualification: the boundary between correcting and rewriting. Fifteen runs, over twelve distinct fixtures, came back with the text unchanged — among them both fixtures the corpus built to tempt a pass into improving competent prose, and the English essay built out of the anti-slop catalogue in concentration, whose Swedish counterpart came back with its punctuation corrected and every one of its patterns intact. Every code sample in both languages came back byte for byte, verified on disk, with misspellings and a split compound left uncorrected inside them and no finding located in one. Every documented refusal was refused before any side effect, with nothing left behind and no permission changed. The language precedence held at every level the corpus stages it: an explicit flag over a map, a map over a Contextual Instruction, an instruction over inference, and inference over nothing — with a suppressed instruction named beside the resolved configuration rather than refused.

What this record does not establish: anything about genre or technique, which this Skill does not resolve; the `handoff-partial` fixture's per-field resolution across all three parameters, of which only the language field is reachable here; and anything about how the Skill behaves in a Harness other than Claude Code.

One ordering note, for the protocol's sake. Every fixture above was judged before any GPT-family material was opened. The opposite family's defect tickets #163 to #166 were read afterwards, while filing the two new ones, and are cited above for that reason; no GPT-family record was opened at any point.

## Runs discarded

None. The routing sentence described under **Run conditions** was carried from the first by-name run onwards, so no run reached the legacy plugin, and no run had to be repeated for any other reason.
