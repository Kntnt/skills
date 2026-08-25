# unslop — claude — 2026-08-25

- **record** — `unslop-claude-2026-08-25`
- **date** — `2026-08-25`
- **ticket** — `#111`
- **skill** — `unslop`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.246
- **corpus commit** — `26155fd`

## Run conditions

The Skill was run as a user of it runs it: `/unslop …` as the whole of a Claude Code turn, against the Skill as installed at `~/.agents/skills/unslop`, reached through `~/.claude/skills/unslop`, which symlinks to it. The installed Skill was byte-identical to `skills/editorial/unslop/` at the corpus commit and the Collection Library it resolves through was byte-identical to `skills/kntnt/`; `diff -r` was run against both before the first run and reported no difference.

Neither was installed that way to begin with. Unslop was not on this machine at all, and the installed Library predated the anti-slop catalogue's current form; both were therefore installed at the corpus commit, with the previous Library kept aside and put back when the runs were finished and the installed Unslop removed again. The machine ends as it began.

Each run was its own Claude Code turn with no memory of any other, driven headless from the user's home directory so that no run read this repository, this ticket, the criteria below, or the Skill's own source tree. Each ran against its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says: `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/111.scratch/runs/<id>`; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form. **side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself.

Two runs were made after that sitting had ended and the install had been taken down again: the two under **Criteria the corpus does not stage on its own** that answer the code half of the preservation criterion. Rather than reinstall globally, they reached the Skill through a project-scoped skills directory holding the same two trees — `unslop` and `kntnt` copied from the corpus commit, checked with `diff -r` the same way — so that nothing outside this ticket's own scratch directory had to be written to. The seam is the same one: `/unslop` typed as the whole of a turn, `$HERE` resolving the checker by the same relative path, and the same Collection Library behind it, all three visible in those two traces. Their turns were driven from the directory that holds that skills directory and nothing else.

Every run inherited `~/.claude/CLAUDE.md`, which every session on this machine inherits. It is recorded because its instructions are visible in some traces — runs cleaned up their own temporary files — and none of them touches editorial behaviour.

Judging was done from the delivered reply, the filesystem inventory, and the run's own recorded tool trace, fixture by fixture, before any GPT-family record existed to compare with. The tool trace is part of the evidence because three of this Skill's obligations are invisible in the reply by design: what a correction subagent was actually given, whether a returned correction was reviewed again, and what the run loaded before reading the text. The Skill's contract keeps that correspondence out of its output, so a record judging it from the output alone could only take the run's word for it. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

`/unslop` is unambiguous on this machine. Peter Yang's `no-ai-slop` Skill is installed beside the Collection's, and answers to a different name; every run below reached the Skill under evaluation with no routing hint, which is visible in each run's own trace: each starts by running the Collection's checker and reading the Collection's `help.md`.

The criterion identifiers are stable across entries:

- `detect` — the catalogue's patterns are found by name rather than as style preference, on Swedish and English instances rather than on the catalogue's English strings.
- `clean` — a text the pass finds nothing in yields no findings and, where the destination is the response or the source itself, the short no-change status rather than a rewritten text.
- `lens` — nothing outside the anti-slop lens is corrected. Mechanical errors present in the fixture are still present afterwards, and genre, technique, and structural expectations are neither imposed nor enforced.
- `no-mechanics` — no mechanical pass is invoked at the end of the run.
- `budget` — the Correction Budget bounds the loop: `0` corrects nothing, a positive value is a ceiling and never a quota.
- `fresh` — every correction is delegated to a subagent started fresh, receiving the complete current text and the complete findings of the most recent pass, handed over directly rather than through a file.
- `verify` — every correction is followed by a fresh re-reading rather than accepted on the corrector's report.
- `stop` — the loop stops where the contract says it stops, and says which of the three conditions stopped it.
- `findings` — findings left over are delivered with the artifact and routed as the contract routes them, a file-targeted run leaving them in the response.
- `language` — the resolved language is the one the precedence names, and it reaches the pass.
- `map` — a recognized `kntnt` map supplies the language and is otherwise left where it is; none is created or synchronized, and nothing outside such a map is read as configuration.
- `preserve` — material the findings do not concern comes through as it arrived, frontmatter, formatting, code, and quotations among it.
- `no-source` — the artifact is never compared with source material and the absence of material is never remarked on.
- `target` — the artifact went where the output contract sends it.
- `effects` — the filesystem shows what the contract allows and nothing else.
- `refusal` — a refused invocation names the problem, prints the synopsis, points at help, and leaves nothing behind.
- `ask` — a materially mixed language produces a question rather than a guess.
- `loading` — only what step 5 names is read: the shared catalogue and the resolved language's anti-slop scope, and no base contract, genre, technique, or other language scope.
- `leak` — the pass's own working, and its correspondence with a correction subagent, stay out of the output.

Forty-nine invocations are recorded below. Forty of them run corpus fixtures; the last nine, under **Criteria the corpus does not stage on its own**, settle four things the corpus supplies no material for — the loop's third stopping condition, the code half of the preservation criterion, three refusals the Skill's own DIAGNOSTICS name and no fixture reaches, and a control that isolates the one failure this run found. Five of those nine staged run-local probe material as `$RUN/probe/` beside `$RUN/corpus/`, quoted in full where it is used. One further entry carries no invocation of its own: `response-default`, which is a situation every destination-less run exercises.

## Prose

### `slop-heavy` (review only)

- **fixture** — `slop-heavy`
- **invocation** — `/unslop --max=0 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back unchanged in the response, followed by findings grouped under the catalogue's own seven headings, every one of them marked unresolved, and a closing note that the `en_GB` scope found nothing.
- **side effects** — none. The inventory is identical before and after.
- **criteria** —
  - `detect` — `pass` — all seven patterns are found by name and quoted individually: the opening sentence and the *But what does this actually mean in practice?* throat-clear, four false contrasts, three unsourced claims, the title formula and the trailing participial clause, five names for one subject, three anaphoric triplets, and the whole closing paragraph.
  - `budget` — `pass` — `0` delegated nothing; the trace carries no subagent at all.
  - `language` — `pass` — `en_GB` inferred from `organisations` and `recognising`, with no flag and no map in play.
  - `no-mechanics` — `pass` — no mechanical pass anywhere in the trace, and the reply says so.
  - `no-source` — `pass` — the three unsourced-claim findings say the *text* carries no source; nothing asks for material or notes its absence.
  - `loading` — `pass` — `anti-slop.md` and the `anti-slop` scope for `en_GB`, and nothing else: no base contract, no genre, no technique, no other scope.
  - `preserve` — `pass` — the returned text is byte-identical to the fixture.
  - `target` — `pass` — no destination named, the response received the artifact.
  - `effects` — `pass` — the inventory is identical before and after.
  - `leak` — `pass` — no reasoning about passages considered and dismissed beyond the one line about the `en_GB` scope, which is a finding-level statement rather than working.
- **unresolved findings** — all of them: eighteen located instances, grouped under the catalogue's seven headings rather than numbered.
- **defects filed** — none.
- **notes** — the corpus's floor for this fixture holds: the review does not find nothing, and no finding is phrased as style preference where the pattern has a name.

### `slop-heavy` (default budget)

- **fixture** — `slop-heavy`
- **invocation** — `/unslop $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a corrected text of five short paragraphs came back in the response, then a paragraph summarising what the eighteen findings were, then one finding left standing after the re-reading.
- **side effects** — none.
- **criteria** —
  - `detect` — `pass` — eighteen findings on the original, covering all seven patterns.
  - `budget` — `pass` — the default of `1` was spent once and no more.
  - `fresh` — `pass` — one subagent, started fresh, whose whole instruction was `correction.md` filled in: the complete current text pasted whole and all eighteen findings verbatim, handed over directly rather than through a file.
  - `verify` — `pass` — the remaining finding is about the *corrected* text — a half-sentence that became the standing claim once the false contrast in front of it was cut — which only a re-reading produces.
  - `stop` — `pass` — the budget was spent with a finding left, and that finding was carried forward and named unresolved.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — no mechanical pass; the reply says so and points at `/proofread` rather than running it.
  - `no-source` — `pass` — nothing about material the run was not given.
  - `loading` — `pass` — the catalogue, the `en_GB` scope, and `correction.md`; nothing else.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing created, replaced, or removed.
  - `leak` — `pass` — the subagent's own account of its work does not appear.
- **unresolved findings** — one: importance inflation in the surviving half of the first paragraph's false contrast.
- **defects filed** — none.
- **notes** — the correction cut roughly four-fifths of the draft, 450 words in and about 90 out, and the corpus's floor rejects *a correction that removes the patterns and the content with them*. This run stays on the right side of it: what went is the empty opening, the generic conclusion, and every claim attributed to nobody — cutting being the catalogue's own prescribed repair for the last, since it forbids furnishing an unsourced claim with a source — and each claim the draft actually supported survives, the distributed-teams one included. The magnitude is recorded because a later reader comparing families will want it.

### `slop-heavy` (budget of three)

- **fixture** — `slop-heavy`
- **invocation** — `/unslop --max=3 $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line saying three passes ran and two of three rounds were spent, then a text of six short paragraphs, then one consequence of the shortening for the reader's eye. No findings.
- **side effects** — none.
- **criteria** —
  - `budget` — `pass` — a ceiling and not a quota: two rounds spent of three, the third left unspent because the pass after round two found nothing.
  - `fresh` — `pass` — two subagents, each started fresh, each given the text as it then stood and the findings of the review immediately before it.
  - `verify` — `pass` — each round is followed by a re-reading from the top, and it is that reading which ends the loop rather than the corrector's report.
  - `stop` — `pass` — stopped on the first of the three conditions, no findings remaining, and says so.
  - `detect` — `pass` — the same patterns found as in the two runs above.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — no mechanical pass in the trace.
  - `loading` — `pass` — the catalogue, the `en_GB` scope, `correction.md`.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
  - `leak` — `pass` — no correspondence with either subagent in the output.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is where Redline's #144 does not repeat. The larger budget converged rather than emptying the text: about 90 words out of 450, the same order as the default-budget run above, with the five substantive claims the draft supported all still present. The reply also volunteers that *"Teams that work this way"* now leans on the heading for its antecedent — an honest consequence of the shortening, offered as a consequence rather than smuggled in as a finding on a run that reported none. One repair is worth a later reader's eye: the second paragraph's importance inflation was repaired by restating the claim plainly rather than by cutting it, where the default-budget run cut it. Both are inside the lens, because what the pattern names is the inflation and not the claim underneath.

### `slop-heavy-sv` (review only, language inferred)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/unslop --max=0 $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete Swedish text came back unchanged in a fenced block, followed by twenty-nine findings located line by line, all marked unresolved. The findings are written in English.
- **side effects** — none.
- **criteria** —
  - `detect` — `pass` — all seven of the shared catalogue's patterns are found on Swedish instances rather than on the catalogue's English strings, and beside them ten of the Swedish scope's own items: the Swedish empty openings and closings, the imported false contrast, the metaphor stock, superlative inflation, the comma after a fronted connective adverb, the em dash, the curly English quotation marks, the serial comma inside a Swedish list, `&` for *och*, the triad reflex twice in one sentence, the wholesale-translated hedging, and authority attributed to nobody. This is the criterion the corpus could not stage before #142, and it is now staged and passed.
  - `budget` — `pass` — `0` delegated nothing.
  - `language` — `pass` — `sv` resolved by inference with nothing naming it, and the scope reached the pass.
  - `no-mechanics` — `pass` — no mechanical pass.
  - `no-source` — `pass` — no remark about material.
  - `loading` — `pass` — the catalogue and the `sv` anti-slop scope, nothing else.
  - `preserve` — `pass` — the returned text is byte-identical to the fixture.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
  - `leak` — `pass` — no working in the output.
- **unresolved findings** — twenty-nine, all of them.
- **defects filed** — #145, by comment; the findings on a Swedish artifact came back in English, where the run below on the same fixture wrote them in Swedish. Nothing in `SKILL.md` or `delivery.md` says which language a findings report is in, though `delivery.md` settles it for the no-change status — which this Skill obeys, in Swedish, on three other Swedish fixtures.
- **notes** — the corpus's floor holds on both halves: the review does not find nothing, and no finding is phrased as style preference where the pattern has a name.

### `slop-heavy-sv` (language named)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/unslop --language=sv $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish header line stating that one correction was spent and the result re-read, then the corrected Swedish text, then six remaining findings in Swedish, each named by its pattern.
- **side effects** — none.
- **criteria** —
  - `detect` — `pass` — twenty-eight findings on the original, which the reply counts as it reports what the correction resolved; the same coverage as the run above.
  - `budget` — `pass` — the default of `1`, spent once.
  - `fresh` — `pass` — one subagent, started fresh, carrying the complete Swedish text and every finding.
  - `verify` — `pass` — all six remaining findings are about the corrected text, and two of them are the corrector's own repairs criticised: a metaphor replaced rather than removed, and a false contrast whose surviving half now opens the piece.
  - `stop` — `pass` — the budget spent with findings left, carried forward as unresolved.
  - `language` — `pass` — `sv` from the flag, and the whole reply is in Swedish.
  - `no-mechanics` — `pass` — none.
  - `no-source` — `pass` — the closing note says the unsourced claims were cut *because the catalogue prescribes cutting rather than furnishing a source*, which is a statement about the catalogue and not a request for material.
  - `loading` — `pass` — the catalogue, the `sv` scope, `correction.md`.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
  - `leak` — `pass` — no correspondence in the output.
- **unresolved findings** — six, all named and located.
- **defects filed** — none.
- **notes** — the corpus's floor rejects *an answer in any language but Swedish*, and this run answers wholly in Swedish. It is the counterpart to the entry above, and the pair is what #145 is about.

### `slop-heavy-sv` (budget of two)

- **fixture** — `slop-heavy-sv`
- **invocation** — `/unslop --max=2 $RUN/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the corrected Swedish text alone, with no findings beside it.
- **side effects** — none.
- **criteria** —
  - `detect` — `pass` — twenty-nine findings on the original, which the run's own narration states before the first round.
  - `budget` — `pass` — two rounds of two; the run counts them down as it goes.
  - `fresh` — `pass` — two subagents, each started fresh.
  - `verify` — `pass` — the narration after round one reads *Re-reading the returned text from the top — two findings survive*, and those two are the second round's brief.
  - `stop` — `pass` — stopped on the first condition with the budget exactly spent and nothing left, which is why the delivery carries the artifact alone.
  - `language` — `pass` — `sv` by inference; the artifact is delivered in Swedish.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue, the `sv` scope, `correction.md`.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
  - `leak` — `pass` — neither corrector's account appears.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — one repair diverges from the run above on the same finding: the vague attribution in the second paragraph was repaired here by removing *Studier visar att* and keeping the claim, where the `--language=sv` run cut the claim entirely, which is what the catalogue prescribes when a text names no source. Both texts are inside the lens — what the pattern names is the borrowed authority — but a later reader comparing families should know that the two repairs of one finding are not the same text, and that the catalogue's own preference is the cut.

### `clean-en-GB`

- **fixture** — `clean-en-GB`
- **invocation** — `/unslop $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — three lines: the language resolved, no findings, and a short no-change status. No text.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings, no rewritten text, and the short status the contract asks for rather than the artifact repeated.
  - `budget` — `pass` — the default went unspent, which is the ceiling-not-quota rule at its cheapest.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor for this fixture rejects *a repeated full text where the contract asks for a short no-change status instead*, and rejects any change to the British forms it plants. Neither happened: `judgement`, `summarise`, `towards`, `fortnight`, and the absent serial comma were never touched, because nothing was.

### `flawed-en-US`

- **fixture** — `flawed-en-US`
- **invocation** — `/unslop $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a four-line resolution summary, then no findings, then a sentence saying that spelling, grammar, punctuation, and the locale's mechanics were neither read against nor corrected here. No text.
- **side effects** — none.
- **criteria** —
  - `lens` — `pass` — the fixture's fourteen mechanical errors — `writen`, `writting`, `It's job`, `Its that`, `into into`, `wasnt`, `dont`, `isnt`, `doesnt`, `would of been`, `The bug were`, `differences was`, `for four year` — are every one of them still there, because nothing was corrected and nothing was rewritten.
  - `clean` — `pass` — no findings and the short status; the anti-slop pass on this text is genuinely empty.
  - `language` — `pass` — `en_US` by inference.
  - `no-mechanics` — `pass` — none, and the reply names the omission explicitly.
  - `loading` — `pass` — the catalogue and the `en_US` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the entry that carries the ticket's third acceptance criterion. The reply also declines a tempting false-contrast reading of the closing *The lesson isn't "rewrite things"*, on the ground that the rejected half is a takeaway the piece itself invites — the catalogue's own carve-out for a contrast that corrects a real belief.

### `flawed-sv`

- **fixture** — `flawed-sv`
- **invocation** — `/unslop $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one Swedish line: *Ingen ändring. Texten har inga anti-slop-fynd, så den lämnas som den är.*
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings, the short status, no text.
  - `language` — `pass` — `sv` by inference, and the status is written in Swedish, which is what `delivery.md` requires of a no-change status.
  - `lens` — `pass` — the fixture's `de`/`dem` error, its särskrivning, its duplicated word, its misspelling, and its missing word are all still there, and `hen` was not touched.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `sv` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the Swedish no-change status is the evidence that `delivery.md`'s one settled language rule is obeyed, which is what makes the English findings report on `slop-heavy-sv` a gap in the contract rather than a Skill ignoring it.

### `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/unslop $RUN/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line: reviewed, clean on all seven patterns, nothing written.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings and the short status.
  - `lens` — `pass` — no technique is resolved, reported, recorded, or acted on. The word *Therefore* opening the third paragraph is not read as evidence of anything, and no structural expectation is applied to a text that nothing selected a shape for.
  - `language` — `pass` — `en_GB`, resolved through the selector `english` and the resource's declared default.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor for this fixture is written for a Skill that has a technique to resolve. Unslop has none, so the floor is met by construction; what the entry establishes is the other half of the ticket's third criterion, that a structural expectation is not imposed on a text just because the text resembles one.

### `mixed-language`

- **fixture** — `mixed-language`
- **invocation** — `/unslop $RUN/corpus/prose/mixed-language.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a question. The run states what it settled — one artifact, default budget, response target, no in-place — then says why it is stopping, quotes the sentence that alternates languages inside itself, lists the three installed resources as candidates, and asks which to read the text against.
- **side effects** — none.
- **criteria** —
  - `ask` — `pass` — a question rather than a guess, asked before anything was read against the catalogue and while nothing had been written.
  - `map` — `pass` — the file has no frontmatter, and the reply says so rather than treating the absence as a problem.
  - `loading` — `pass` — the catalogue was not loaded at all, because the language was never settled.
  - `target` — `pass` — nothing delivered, which is correct for a run that stopped to ask.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor is *a language silently picked and acted on*, and the run does the opposite: it names the candidates and offers the flag form that would settle it.

### `locale-divergent` (British English)

- **fixture** — `locale-divergent`
- **invocation** — `/unslop --language=en_GB $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no findings and a short no-change status, with a sentence saying the British guidance turned up no reskinning tell.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings, no rewritten text.
  - `language` — `pass` — `en_GB` from the flag, and the `en_GB` scope is the one that reached the pass.
  - `lens` — `pass` — the ambiguous numeric date `3/4` was not rewritten into an unambiguous one, and `organised`, `licence`, and the pound figure were not treated as errors.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

### `locale-divergent` (American English)

- **fixture** — `locale-divergent`
- **invocation** — `/unslop --language=en_US $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no findings and a short no-change status, with a parenthesis saying spelling and locale mechanics are outside this pass and were left as they arrived.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings, no rewritten text.
  - `language` — `pass` — `en_US` from the flag; the American scope is the one loaded.
  - `lens` — `pass` — the British forms the fixture plants are not treated as errors under the American locale, because the mechanics are not this pass's to touch under either. `3/4` stays ambiguous.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_US` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the fixture asks to be run under each English locale in turn. For a Skill contracted to mechanics the two runs would diverge; here they converge, and the convergence is the point: the resolved locale reaches the pass and selects a different scope, and neither scope has an opinion about a divergent spelling.

## Source material

### `brief-short`

- **fixture** — `brief-short`
- **invocation** — `/unslop ` followed by the whole of `source/brief-short.md`, pasted inline as the operand
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a new 378-word article. The run opened by saying *`/unslop` reviews an existing text … it doesn't write. What you passed is a brief, so I wrote the piece and applied the anti-slop lens to it as I went*, then delivered the piece, then closed by naming two of its own passages as *my inference, not facts you gave me*.
- **side effects** — none.
- **criteria** —
  - `lens` — `fail` — an unsupported fact. The delivered artifact carries material the supplied text does not: a paragraph on why the Monday deadline works and a paragraph on why the Thursday call works, both of which the run itself identifies as its own inference. Nothing here is the anti-slop pass, and everything here is outside the lens.
  - `clean` — `fail` — the brief's own prose is clean against the catalogue, and the contract's answer to that is the short no-change status. What came back was a new document.
  - `loading` — `fail` — the run never read `help.md`, never resolved a language, and never loaded any language's anti-slop scope. It ran the checker, read `anti-slop.md`, and wrote.
  - `budget` — `skipped` — no correction loop ran, so there was no budget behaviour to observe.
  - `no-mechanics` — `pass` — no mechanical pass, which is the one part of the contract the run did not break.
  - `effects` — `pass` — nothing was created, replaced, or removed.
- **unresolved findings** — none, and none were recorded.
- **defects filed** — #147.
- **notes** — the corpus supplies this fixture as inline material and its floor is *a draft that reports a benefit the brief does not contain*. The floor is written for Write, and this run is not Write, but the run produced a draft anyway and the floor catches it: the brief says nobody asked to go back and says nothing shipped faster, and the article respects both — while adding reasoning about two decisions that the brief never explains. The failure is not about inline supply. `slop-heavy` pasted inline the same way ran the whole flow correctly, and that run is recorded under **Criteria the corpus does not stage on its own** as the control that isolates this one.

### `brief-article-abt`

- **fixture** — `brief-article-abt`
- **invocation** — `/unslop --genre=article --technique=abt $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a refusal naming both flags as undeclared, the SYNOPSIS verbatim, a pointer at `/unslop --help`, a sentence saying this Skill selects no genre and no technique so there is nothing for those flags to do, and the valid invocation that drops them.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — names what was wrong in one line, prints the synopsis, points at help, and says nothing was read and nothing written.
  - `lens` — `pass` — the two flags are refused rather than ignored, which is the strongest form of the rule that no genre and no technique enter this Skill.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus supplies this fixture with the instruction to select the article genre and the ABT technique. Unslop has neither option, so the fixture's own staging is what produces the refusal, and that is the useful thing it establishes here.

### `brief-report-pac`

- **fixture** — `brief-report-pac`
- **invocation** — `/unslop $RUN/corpus/source/brief-report-pac.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line: read as `en_GB`, no findings, budget unspent, nothing written.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings and the short status.
  - `lens` — `pass` — no genre and no technique resolved or reported, on material the corpus stages as a report-and-PAC fixture.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the brief carries a stated counter-argument, and the corpus's floor rejects resolving it by inventing evidence. Nothing was resolved and nothing invented, because nothing was changed.

### `brief-press-release-sv` (language inferred)

- **fixture** — `brief-press-release-sv`
- **invocation** — `/unslop $RUN/corpus/source/brief-press-release-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish no-change status naming each of the seven patterns as absent, saying the budget is unspent and nothing was written.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings, no text.
  - `language` — `pass` — `sv` by inference with nothing naming it, and the status is in Swedish.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `sv` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor rejects *a draft in any language but Swedish when nothing overrode inference*, and the answer here is Swedish throughout.

### `brief-press-release-sv` (language named by alias)

- **fixture** — `brief-press-release-sv`
- **invocation** — `/unslop --language=svenska $RUN/corpus/source/brief-press-release-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the same Swedish no-change status, prefaced by a line naming the resolved resource.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings, no text.
  - `language` — `pass` — the curated alias `svenska` reached `sv` through the resolver, and the reply names `sv` as what it resolved to.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `sv` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the fixture asks for one inferred run and one named run, and this is the named one. It also exercises the alias rather than the canonical code, which the flag's own documentation promises and no other entry in this record reaches.

### `interview-transcript`

- **fixture** — `interview-transcript`
- **invocation** — `/unslop --max=0 $RUN/corpus/source/interview-transcript.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a resolution line, then no findings, with a sentence saying the disfluencies and repetitions are the verbatim speech the header declares.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings on material whose surface invites a great many.
  - `lens` — `pass` — the spoken syntax, the fillers, the repetition, and the self-correction from eleven-plus-others to eleven are all left exactly where they are, and the run says why: the header declares the text a verbatim transcript.
  - `no-source` — `pass` — nothing asks for the recording, the article the transcript is for, or any other material, and nothing remarks that none was supplied. This is the fixture where such a remark would be most tempting.
  - `language` — `pass` — `en_GB` inferred from `tyre` and `11 March`.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor for this fixture is written about quotations in a draft, which this run produces none of. What the entry establishes is that the transcript survives the pass untouched, and that the Skill does not read a transcript's broken syntax as robotic rhythm's opposite extreme.

### `factual-source-long`

- **fixture** — `factual-source-long`
- **invocation** — `/unslop --max=0 $RUN/corpus/source/factual-source-long.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a resolution line naming the evidence for `en_GB`, then no findings, with a sentence explaining why the parallel figures in *What was measured* are comparison rather than template.
- **side effects** — none.
- **criteria** —
  - `clean` — `pass` — no findings on eight hundred words of dated, attributed material.
  - `no-source` — `pass` — a long factual document with an eighteen per cent response rate, a stated estimate, and a section of its own limits, and the run does not once remark that it cannot check any of it.
  - `lens` — `pass` — the numbers, the caveats, and the closing limits section are untouched, and no structural expectation is applied to a document nothing selected a genre for.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

### `url-source` (review only)

- **fixture** — `url-source`
- **invocation** — `/unslop --max=0 https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one line: read as `en_US`, no findings, nothing changed, nothing written.
- **side effects** — none inside the working copy. The run fetched the RFC to `/tmp/rfc2119.txt` and removed it again in its last tool call; that path is outside `$RUN` and outside any destination the delivery contract governs.
- **criteria** —
  - `clean` — `pass` — no findings on a published RFC.
  - `language` — `pass` — `en_US` by inference.
  - `no-source` — `pass` — the material *is* a source document, and nothing about verification appears.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_US` scope.
  - `target` — `pass` — response; a URL as material selects no destination.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor rejects *any definition attributed to the RFC that the RFC does not give*, and this run attributes nothing because it changes nothing. The temporary fetch is recorded because a later reader comparing families will want to know it happened and that it was cleaned up; whether a run may write outside its Output Target at all is not a question `delivery.md` reaches, and nothing here turns on it.

### `url-source` (In-place Editing refused)

- **fixture** — `url-source`
- **invocation** — `/unslop --in-place https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — n/a; the invocation was refused
- **observed delivery** — a refusal in one line — a URL is not a writable local file to replace — then the SYNOPSIS verbatim, a pointer at help, and *Nothing was read and nothing was written.*
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — names the problem, prints the synopsis, points at help, leaves nothing behind.
  - `effects` — `pass` — nothing fetched, nothing written; the refusal was made by reading the invocation alone.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor for this fixture names exactly this refusal.

## Frontmatter

### `handoff-present` (map supplies the language)

- **fixture** — `handoff-present`
- **invocation** — `/unslop $RUN/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line saying the language was resolved to `en_GB` *from the artifact's own `kntnt` frontmatter map*, then no findings and a short no-change status.
- **side effects** — none.
- **criteria** —
  - `map` — `pass` — the map's `language` is read and used; the reply says so. The map's `genre` and `technique` are not reported, not resolved, and not acted on, because this Skill has no such parameters.
  - `language` — `pass` — `en_GB`, taken from level 2 of the resolution order with nothing above it.
  - `clean` — `pass` — no findings, no text.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor rejects *the map's values reported back in a spelling other than the normalized ones it carries*, and the reply gives `en_GB` exactly as the map writes it.

### `handoff-present` (unchanged, written to a named file)

- **fixture** — `handoff-present`
- **invocation** — `/unslop --output=$RUN/out/kept.md $RUN/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/kept.md`
- **observed delivery** — a sentence saying the text was clean and that an explicitly named destination still receives the complete artifact when nothing changed, then the destination, its size, and a note that the source is untouched and no mechanical pass ran.
- **side effects** — `out/kept.md` created. Nothing else created, replaced, or removed.
- **criteria** —
  - `map` — `pass` — this is the entry that settles the synchronization half. The written file is byte-identical to the fixture, so the three-key `kntnt` map came through exactly as it arrived: not rewritten, not reordered, not synchronized to the run's resolved configuration, and nothing added beside it.
  - `preserve` — `pass` — byte-identical, frontmatter and body alike.
  - `clean` — `pass` — the pass found nothing, and the run did not invent something to justify the file it was asked to write.
  - `target` — `pass` — an explicitly named non-existing path received exactly that one file, and the unchanged result was still delivered to it, which is what `delivery.md` requires.
  - `effects` — `pass` — one file created, no directory made, the source untouched.
  - `no-mechanics` — `pass` — none, and the reply says so.
  - `language` — `pass` — `en_GB` from the map.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this entry and `handoff-unusable` (flag) between them cover the ticket's map criterion in both directions: a map that is used and left alone on an unchanged artifact, and a map that is used, superseded, and still left alone on a changed one.

### `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/unslop --language=sv $RUN/corpus/frontmatter/handoff-conflicting.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish no-change status naming the seven patterns as absent, and an italic closing line saying the language came from `--language=sv`, which outranks `kntnt.language: en_US`, and that the frontmatter was left untouched.
- **side effects** — none.
- **criteria** —
  - `map` — `pass` — the map is recognized, its `language` is superseded by the flag rather than ignored or silently obeyed, and the run states which level won. Nothing in the frontmatter changed.
  - `language` — `pass` — `sv` from level 1, against a map saying `en_US` and a body written in Swedish.
  - `clean` — `pass` — no findings, no text.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `sv` scope; the `en_US` scope was never loaded.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor rejects *the file delivered with a Kntnt map still contradicting the configuration the run actually resolved*. That floor is written for a Skill that synchronizes; Unslop's contract says the opposite, that no map is created or synchronized because it settles only one of the three values such a map records. Nothing was delivered to a file here in any case, so the two never meet; the entry below on `handoff-unusable` is where a contradicting map does survive a delivery, deliberately.

### `handoff-partial`

- **fixture** — `handoff-partial`
- **invocation** — `/unslop $RUN/corpus/frontmatter/handoff-partial.md -- Texten är på svenska.`
- **contextual instruction** — `Texten är på svenska.`
- **output target** — `response`
- **observed delivery** — a line saying the re-reading found nothing left and that the source is untouched, then the complete artifact, frontmatter included.
- **side effects** — none.
- **criteria** —
  - `map` — `pass` — the one-key map is neither a reason to stop nor a reason to ask for a complete one, and it is not read as unusable metadata. Its `technique` key is not acted on, because this Skill has no technique. The delivered artifact still carries the map with its single key, uncompleted and unsynchronized.
  - `language` — `pass` — level 1 supplies nothing, level 2 has no `language`, and the Contextual Instruction at level 3 settles `sv`. No language question was asked, which is correct: the instruction had already named one.
  - `preserve` — `pass` — the delivered text differs from the fixture in exactly one character. Everything else, frontmatter and the whole English-and-Swedish body, is byte-identical.
  - `detect` — `pass` — the one finding is from the Swedish scope's own list rather than from the shared catalogue: the unspaced em dash where Swedish takes a spaced en dash. That is the language resource reaching a finding on its own, in a fixture the corpus supplies for resolution rather than for detection.
  - `budget` — `pass` — the default of `1`, spent once.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — the returned text was re-read, and it is that reading which reports nothing left.
  - `stop` — `pass` — stopped on the first condition, no findings remaining.
  - `no-mechanics` — `pass` — none. Worth stating on this entry in particular: the one change is a punctuation change, and it is inside the lens because the Swedish anti-slop scope names it. Nothing else about the text's punctuation, spelling, or grammar was touched.
  - `loading` — `pass` — the catalogue and the `sv` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the fixture #142 added, and it does the work the ticket's language-precedence criterion asks for: a level-3 value settling what levels 1 and 2 leave open, over a map that exists, is recognized, and is left exactly as it was.

### `handoff-unusable` (no flag)

- **fixture** — `handoff-unusable`
- **invocation** — `/unslop $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a stop. The reply is headed *Unusable artifact metadata — run stopped*, quotes the map, lists the three installed resources, says that `en_UK` reaches none of them and never becomes `en_GB` on its own, and offers two ways forward — supersede it with `--language`, or correct the map — adding that the Skill will not write the map itself.
- **side effects** — none.
- **criteria** —
  - `map` — `pass` — the map is recognized, its unusable value stops the run rather than being quietly reinterpreted, and the reply says explicitly that this Skill neither edits nor creates such a map.
  - `refusal` — `pass` — names the problem, quotes the evidence, and reports that nothing was read against the catalogue and nothing written.
  - `loading` — `pass` — the catalogue was never loaded, because the language never resolved.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor is `en_UK` quietly read as `en_GB`, and the reply refuses that by name.

### `handoff-unusable` (flag supersedes)

- **fixture** — `handoff-unusable`
- **invocation** — `/unslop --language=en_GB $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete artifact, corrected, with nothing else beside it.
- **side effects** — none.
- **criteria** —
  - `map` — `pass` — the strongest evidence in this record. A flag at level 1 suppressed the unusable value, the run proceeded, made a change, and delivered the artifact **with the `en_UK` map still in it**, unchanged and unsynchronized. Compare the run above, where the same map with no flag stops the run: one flag decides whether the same metadata is fatal, and in neither case is it edited.
  - `language` — `pass` — `en_GB` from the flag, and the finding it produced comes from the `en_GB` scope.
  - `detect` — `pass` — one finding, from the British scope's *apologetic opening* item: *it is worth noting that*.
  - `preserve` — `pass` — the delivered text differs from the fixture only by that clause. The frontmatter, both paragraphs, and every figure are byte-identical.
  - `budget` — `pass` — the default of `1`, spent once.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — the returned text was re-read and reported clean.
  - `stop` — `pass` — first condition, no findings remaining.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

### `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/unslop $RUN/corpus/frontmatter/frontmatter-unrelated.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line naming `lang: fr`, `genre: fiction`, `technique: montage`, and `language: Esperanto` as the document's own keys rather than a `kntnt` map, then no findings and a short no-change status, then two passages the run looked at and left alone with its reasons.
- **side effects** — none.
- **criteria** —
  - `map` — `pass` — all four bait keys are named and refused as configuration, and the run says why: they are not inside a `kntnt` map. No map was added.
  - `language` — `pass` — `en_GB` by inference from the text, with `fr` and `Esperanto` sitting in the frontmatter and reaching nothing.
  - `clean` — `pass` — no findings, no text, and so no change to the frontmatter block.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
  - `leak` — `pass` — the two passages it names are findings it considered and rejected, stated as conclusions rather than as working. This is the one entry where the line is close, and the reply stays on the right side of it: each is one sentence saying why the pattern is absent, which is what a reader of a clean verdict on a text containing a negation and an unnamed authority needs.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the two passages are worth recording for a family comparison, because both are near misses the catalogue explicitly carves out: a contrast that corrects a real belief, and an unnamed body that is the foil being contradicted rather than an authority being borrowed from.

### `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/unslop $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line saying the synonym cycling is repaired and the re-read comes back clean, then the complete artifact, then one paragraph naming the finding and its repair: four words changed, no sentence rewritten.
- **side effects** — none.
- **criteria** —
  - `map` — `pass` — no metadata was demanded, no refusal made, and no `kntnt` map added to a file that has no frontmatter at all. The reply states that the file carries none and that nothing in it was read as configuration.
  - `detect` — `pass` — the finding is genuine synonym cycling: the same object is *roster* in the heading and first paragraph and *rota* four times afterwards, the two names meeting inside one sentence.
  - `preserve` — `pass` — four words changed and nothing else; every sentence, every clause, and the spaced em dashes come through as they arrived.
  - `budget` — `pass` — the default of `1`, spent once.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — the returned text was re-read and reported clean.
  - `stop` — `pass` — first condition.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this run also stands for `response-default`, below.

## Output situations

### `response-default`

- **fixture** — `response-default`
- **invocation** — none of its own. Thirty-five of the forty-nine invocations in this record name neither `--output` nor `--in-place`, and each of them is this situation.
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — in every one of those runs, the result came back in the response and nothing else.
- **side effects** — none, in every one of them. Forty-one of the forty-nine before-and-after inventories are identical, and the eight that are not belong to the eight runs that named a file or a directory.
- **criteria** —
  - `target` — `pass` — the default was kept wherever it was not overridden, and supplying a local file as material never selected a destination.
  - `effects` — `pass` — no file created, replaced, or removed anywhere under `$RUN` by any run that named no destination.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor for this situation is exactly the second criterion, and it holds across every destination-less run in this record.

### `new-file`

- **fixture** — `new-file`
- **invocation** — `/unslop --output=$RUN/out/unslopped.md $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/unslopped.md`
- **observed delivery** — the destination, the resolved language, the budget spent and the re-reading that followed it, and a note about the magnitude of the shortening. No artifact in the response.
- **side effects** — `out/unslopped.md` created. Nothing else created, replaced, or removed; the source is untouched.
- **criteria** —
  - `target` — `pass` — exactly that one file at exactly that path.
  - `effects` — `pass` — no sibling written beside it, no directory made, no partial file.
  - `budget` — `pass` — one round, the default.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — the re-read found nothing left, and the reply says so.
  - `stop` — `pass` — first condition.
  - `detect` — `pass` — the same patterns as the response-targeted runs on this fixture.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue, the `en_GB` scope, `correction.md`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor rejects a run that *creates the file and also prints the whole artifact as though no destination had been given*, and this run prints none of it. The `new-file` situation is exercised twice more in this record, by `handoff-present` written to a named file and by the unchanged-result entry below.

### `existing-file`

- **fixture** — `existing-file`
- **invocation** — `/unslop --output=$RUN/corpus/output/existing-target.md $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — the destination and the fact that it replaced what was there, the resolved language, two unresolved findings written out in full, a paragraph listing what was repaired, and a closing line saying no mechanical pass ran. No artifact in the response.
- **side effects** — `corpus/output/existing-target.md` replaced; its checksum differs before and after and no other path moved. The source `slop-heavy.md` is untouched.
- **criteria** —
  - `target` — `pass` — the exact existing path was overwritten, with no extra confirming flag demanded and none offered, and no sibling written beside it.
  - `effects` — `pass` — one file replaced and nothing else.
  - `findings` — `pass` — a file-targeted run left its two unresolved findings in the response, which is where the contract puts them.
  - `budget` — `pass` — one round, the default, spent.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — one of the two remaining findings is a partially repaired one, named as such, which only a re-reading of the corrected text produces.
  - `stop` — `pass` — the budget spent with findings left, carried forward.
  - `no-mechanics` — `pass` — none, and the reply says so and points at `/proofread` instead.
  - `language` — `pass` — `en_GB` by inference.
  - `loading` — `pass` — the catalogue, the `en_GB` scope, `correction.md`.
- **unresolved findings** — two: an empty opening in the third paragraph, and importance inflation in a claim the repair restated rather than cut.
- **defects filed** — none.
- **notes** — the corpus's floor rejects *a demand for an extra confirming flag, a sibling written beside it, and the occupant left in place while the result went elsewhere*. None of the three happened.

### `existing-directory`

- **fixture** — `existing-directory`
- **invocation** — `/unslop --output=$RUN/out $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the derived path, a note that the name came from the source basename with no collision, the resolved language, seventeen findings recorded and one correction delegated and re-read, then the one unresolved finding. No artifact in the response.
- **side effects** — `out/slop-heavy.md` created. Nothing written outside the named directory; the source is untouched.
- **criteria** —
  - `target` — `pass` — the filename is derived from the source basename and keeps its `.md` extension; nothing is named for the directory.
  - `effects` — `pass` — one file inside the named directory and nothing anywhere else.
  - `budget` — `pass` — one round, the default.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — the remaining finding is about the corrected text.
  - `stop` — `pass` — budget spent with a finding left, carried forward.
  - `no-mechanics` — `pass` — none.
  - `language` — `pass` — `en_GB` by inference.
  - `loading` — `pass` — the catalogue, the `en_GB` scope, `correction.md`.
- **unresolved findings** — one: importance inflation in the surviving half of a false contrast.
- **defects filed** — none.
- **notes** — none.

### `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/unslop --output=$RUN/corpus/output/collision $RUN/corpus/output/interview-notes.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the derived path `interview-notes-3.md`, a sentence explaining that the directory already held the first two names so the sequence took the next free number, and a note that the pass found nothing so the budget went unspent.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants are byte-identical before and after.
- **criteria** —
  - `target` — `pass` — the stem stayed `interview-notes` and the first free candidate in ascending order was taken. No numbered candidate was adopted as a new stem, so nothing is named `interview-notes-2-2.md`.
  - `effects` — `pass` — neither occupant overwritten, one file added, nothing else touched.
  - `clean` — `pass` — the pass found nothing, and the unchanged artifact was still written because a directory destination was explicitly chosen.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor names both halves of this — an occupant overwritten, and a name built by suffixing the colliding candidate — and neither happened.

### `read-only-source`

- **fixture** — `read-only-source`
- **invocation** — `/unslop --in-place $RUN/corpus/output/readonly-source.md`
- **contextual instruction** — `none`
- **output target** — n/a; the invocation was refused
- **observed delivery** — a refusal naming the file's mode as `444` and In-place Editing's requirement of exactly one writable local source file, then the SYNOPSIS verbatim and a pointer at help, with a sentence saying nothing was read against the catalogue and nothing written.
- **side effects** — none. The file's permissions are unchanged and its checksum is identical.
- **criteria** —
  - `refusal` — `pass` — names the problem with the evidence, prints the synopsis, points at help.
  - `effects` — `pass` — no permission changed to make the write possible, no result written elsewhere as a silent substitute, no partial effect left behind. The corpus's floor names all three, and none happened.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

### `in-place-request`

- **fixture** — `in-place-request`
- **invocation** — `/unslop --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place
- **observed delivery** — a paragraph saying the text is clean on all seven patterns, with the reason two near misses are not findings, then the budget unspent, then the short no-change status. No text, and no file written.
- **side effects** — none. The source is byte-identical before and after.
- **criteria** —
  - `clean` — `pass` — an in-place run that found nothing wrote nothing and returned a short status, which is what `delivery.md` requires: rewriting a file with its own contents would make its timestamp claim that something happened.
  - `target` — `pass` — In-place Editing was accepted for the one case it is available for, a writable local file, and no copy was left beside it.
  - `effects` — `pass` — nothing created, replaced, or removed.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
  - `loading` — `pass` — the catalogue and the `en_GB` scope.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus's floor rejects *a rewritten file where the run found nothing to change and a short status was the contract*, which is exactly the case this run met. The two near misses the reply names — the parallel `It is…` construction and the closing repetition of *being read during an incident* — are the catalogue's carve-out for a repetition that lands.

### `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/unslop --output=$RUN/corpus/output/in-place-source.md $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — n/a; the invocation was refused
- **observed delivery** — a refusal in one line — the output path is the same path as the Text Artifact, use `--in-place` to replace a source — then the SYNOPSIS verbatim, a pointer at help, a statement that nothing was read and nothing written, and the corrected invocation.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — names the problem, prints the synopsis, points at help, and names the gesture to use instead, which the contract requires of this refusal specifically.
  - `effects` — `pass` — the file is byte-identical; the refusal was made by comparing two paths before anything was read.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

### `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/unslop --output=$RUN/out/both.md --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — n/a; the invocation was refused
- **observed delivery** — a refusal in one line — both were given, naming two destinations for one text — then the SYNOPSIS verbatim, a pointer at help, and *Nothing was read and nothing was written.*
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — names the problem, prints the synopsis, points at help.
  - `effects` — `pass` — neither half executed: `out/both.md` does not exist and the source is byte-identical. The corpus's floor is exactly that no side effect precedes the refusal.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

### `new-file` (unchanged result)

- **fixture** — `new-file`
- **invocation** — `/unslop --output=$RUN/out/clean.md $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/clean.md`
- **observed delivery** — *The pass found nothing. Written to …, unchanged from the source.* — and then the complete four-paragraph artifact printed into the response as well.
- **side effects** — `out/clean.md` created, byte-identical to the source. Nothing else.
- **criteria** —
  - `clean` — `pass` — the pass found nothing and nothing was invented to justify the file.
  - `target` — `pass` — the unchanged result still reached the explicitly named destination, which is what `delivery.md` requires, and the file is byte-identical to the source.
  - `effects` — `pass` — one file created, no directory made, the source untouched.
  - `language` — `pass` — `en_GB` by inference.
  - `no-mechanics` — `pass` — none.
- **unresolved findings** — none.
- **defects filed** — #148.
- **notes** — this is the one file-targeted run of seven that also printed the whole artifact into the response, and the artifact it printed was byte-identical to the source the caller already had. The corpus's `new-file` floor rejects that shape, and `delivery.md` does not reach the question: it settles what a response-targeted run delivers and says nothing about what a file-targeted one may put in the response beside its findings. The other six printed no text at all — `handoff-present` written to a named file among them, which is the other run whose pass found nothing and which wrote its file in silence.

### `existing-directory` (filename derived from a URL)

- **fixture** — `url-source`, delivered into `existing-directory`
- **invocation** — `/unslop --max=0 --output=$RUN/out https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — no findings, a paragraph saying why each of the seven patterns is absent from RFC 2119, and the derived path, with a note that the name comes from the URL's title because a URL supplies no local basename, that `.txt` was carried over, and that the directory was empty so no collision numbering applied.
- **side effects** — `out/key-words-for-use-in-rfcs-to-indicate-requirement-levels.txt` created, byte-identical to the fetched source. Nothing else.
- **criteria** —
  - `target` — `pass` — the filename derives from the URL's title, which is the second of the three sources `delivery.md` names, and it keeps a suitable text extension. Nothing was written outside the named directory.
  - `clean` — `pass` — the unchanged artifact was still written, because a directory destination was explicitly chosen.
  - `effects` — `pass` — one file, and the run's own `sha256` check against the source agrees with the inventory.
  - `budget` — `pass` — `0`, with nothing to spend.
  - `language` — `pass` — `en_US` by inference.
  - `no-mechanics` — `pass` — none.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the third of the three filename sources `delivery.md` lists; the source basename is exercised by `existing-directory` and `derived-name-collision` above, and the Skill's own working title has no case here because Unslop creates no text.

## Criteria the corpus does not stage on its own

Four things the ticket asks for have no fixture. The loop's third stopping condition needs a correction that makes no relevant progress, and every corpus fixture that reaches the loop at all either converges or leaves findings the budget ran out on. The preservation criterion names code, and the corpus carries none: ``grep -rl '`' ../corpus/`` and `grep -rlE '^    \S' ../corpus/` reach no fixture prose, and the index's coverage vocabulary has no tag for it. That gap is filed as #150 rather than closed here by adding to the corpus. Three of the refusals the Skill's own DIAGNOSTICS section names have no fixture either. And the failure recorded above on `brief-short` needed a control before it could be filed against the right thing.

These nine invocations were made under the same harness and the same before-and-after inventory as the forty above, and under the same install but for the last two, whose route is in **Run conditions**. Five of them staged run-local material as `$RUN/probe/` beside `$RUN/corpus/`, which is quoted in full where it is used. Nothing in the corpus was touched: no fixture, no index entry, and no floor, so `corpus commit 26155fd` still says what it said and the GPT-family run has the same material to answer.

### `probe/single-finding.md` — the loop's third stopping condition

The material is three lines, and its whole body is one sentence the catalogue names as an empty opening:

```markdown
# Note for the board

Communication has never been more important.
```

- **fixture** — none; run-local probe material
- **invocation** — `/unslop --max=2 $RUN/probe/single-finding.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line saying the correction round returned the text with nothing changed and that re-reading it leaves the finding standing, so the loop stopped there with one unit of the budget unspent; then the artifact; then the one finding, marked unresolved, with the reason it cannot be repaired.
- **side effects** — none.
- **criteria** —
  - `stop` — `pass` — the third of the three conditions, reached and named: a round whose re-reading leaves the finding it was given standing with nothing it named changed. The loop stopped rather than spending the second round on the same round again.
  - `budget` — `pass` — `2` given, one spent, one left unspent by the stop rather than by exhaustion.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — the corrector's report is not what ended the loop; the re-reading is.
  - `detect` — `pass` — the finding is correct, and its reason is the catalogue's own: cutting the sentence leaves a heading with nothing under it, and writing a real opening would mean inventing what the board is being told.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — one.
- **defects filed** — none.
- **notes** — with `probe-quoted-sv` and `probe-quoted-en` below, and the corpus runs above, all three stopping conditions are now on record: no findings with budget unspent (`slop-heavy` at `--max=3`, `slop-heavy-sv` at `--max=2`, and five more), the budget spent with findings left (`slop-heavy` and `slop-heavy-sv` at the default, `existing-file`, `existing-directory`), and no relevant progress, here.

### `probe/quoted-slop-sv.md` and `probe/quoted-slop-en.md` — a first attempt at the same condition

Two texts, one Swedish and one English, whose own prose is clean and whose every catalogued pattern sits inside a block quotation attributed to a named person and marked as verbatim. The Swedish one reads:

```markdown
# Vad kvartalsrapporten säger

Bolaget redovisade en omsättning på 84 miljoner kronor för kvartalet, mot 79 miljoner samma kvartal i fjol. Antalet anställda är oförändrat, 212. Utdelningen är ännu inte beslutad.

Vd Karin Ohlsson kommenterade siffrorna i ett uttalande till personalen den 3 oktober, som citeras ordagrant här:

> Det här är ett paradigmskifte för oss. I dagens snabbrörliga värld är det inte bara en fråga om siffror — det handlar om att verkligen förstå kraften i det vi bygger. Studier visar att de bolag som vågar satsa tidigt får ett försprång som är svårt att hämta in. Sammanfattningsvis är nyckeln till framgång att vi fortsätter på den inslagna vägen.

Styrelsen tar ställning till utdelningen den 14 november. Ohlsson har inte kommenterat den frågan.
```

The English one is the same shape with the same patterns.

- **fixture** — none; run-local probe material
- **invocation** — `/unslop --max=2 $RUN/probe/quoted-slop-sv.md` and `/unslop --max=2 $RUN/probe/quoted-slop-en.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — both returned a short no-change status. The Swedish one says the patterns in the document sit entirely inside the block quotation, which is Ohlsson's words reproduced verbatim, and that editing them away would be a misquotation rather than an edit.
- **side effects** — none, in either.
- **criteria** —
  - `preserve` — `pass` — this is the entry that carries the quotation half of the ticket's preservation criterion. A text whose slop is all inside a verbatim quotation is left alone entirely, and the Swedish run says why in a sentence.
  - `clean` — `pass` — the short status, in the artifact's own language in the Swedish case.
  - `stop` — `skipped` — these two runs were staged to reach the loop's third condition and did not: neither delegated a correction, because neither found a finding to correct. The condition is reached by `probe/single-finding.md` above instead.
  - `effects` — `pass` — nothing written by either.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the attempt failed and the result is worth more than the attempt would have been. A pass that treats a verbatim quotation as the writer's prose would have produced the stopping condition by refusing to repair it; what happened instead is that the pass never called it a finding, which is the better behaviour and the one the correction brief's own instruction about quotations anticipates.

### `probe/code-slop-en.md` — the code half of the preservation criterion

The material is an article whose prose carries the catalogue's patterns and which also carries code the prose does not concern: a fenced Python block, an indented block, and two inline spans. The prose *inside* the code carries the same patterns as the article around it, the identifiers are named after two of those patterns, and the exception message holds a misspelling. A pass that read a code sample as the writer's prose, or that reached for the mechanical layer on the way past, would therefore leave a mark impossible to miss:

`````markdown
# Unlocking the Power of Retry Logic in Modern Distributed Systems

In today's fast-paced engineering landscape, the way services recover from failure has never been more important. It's not just about resilience — it's about fundamentally rethinking how systems behave under pressure. Studies show that most outages begin as a transient error nobody handled.

The naive approach is a fixed delay. Consider the following implementation, which many teams still ship:

```python
def retry(fn, attempts=5):
    """In today's fast-paced world, retrying is not just about resilience —
    it's about survival. Studies show that most failures are transient.

    At the end of the day, the key to success is patience."""
    for i in range(attempts):
        try:
            return fn()
        except TransientError:
            # It's not just a delay — it's a backoff. This is a paradigm shift.
            time.sleep(2 ** i)
    raise ExhaustedError("Furthermore, the recieved response never arrived.")
```

But what does this actually mean in practice? At its core, exponential backoff is about respecting the server. It's about acknowledging that a struggling service needs room. It's about recognising that every client retrying in lockstep is a thundering herd.

The remedy is jitter. Experts agree that full jitter is the right default, and the change is a single expression. Call `not_just_about()` on the delay, or set the module flag `STUDIES_SHOW = True`, and the sleep becomes:

    # In conclusion, the key to success is randomness.
    sleep = random.uniform(0, min(cap, base * 2 ** i))
    log.debug("It is worth noting that the delay was %s", sleep)

Teams report fewer cascades. Teams report shorter incidents. Teams report calmer on-call rotations. Furthermore, jittered backoff enables distributed clients to spread their load seamlessly across the recovery window, fostering a healthier system where every request can be served, regardless of when the failure began.

At the end of the day, the future of resilience isn't about choosing between retrying and failing fast. It's about finding the right balance for your unique system and context. One thing is certain: the teams that thrive in the years ahead will be those that master this balance.
`````

Two runs, differing in the Correction Budget and the destination. The first reviews without correcting, which shows what the pass calls a finding; the second corrects twice into a file, which shows what survives a run that does change the text. Preservation is only testable on the second: a text nothing happened to proves nothing about what a repair leaves alone.

#### `probe/code-slop-en.md` (review only)

- **fixture** — none; run-local probe material
- **invocation** — `/unslop --max=0 $RUN/probe/code-slop-en.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete text came back in the response, followed by fifteen located findings, every one of them unresolved, each given by line and named by its pattern.
- **side effects** — none. The inventory is identical before and after.
- **criteria** —
  - `preserve` — `pass` — the returned text is byte-identical to the fixture, `sha256` `e589024d…`, code and prose alike. `--max=0` is a review, and a review returns the artifact rather than a version of it.
  - `detect` — `pass` — six of the catalogue's seven patterns, each found by name: the title's inflation, the empty opening and the false contrast and *Studies show* in the first paragraph, the *But what does this actually mean in practice?* throat-clear, two anaphoric triplets, *Experts agree*, the trailing participial clause, and the whole closing paragraph. The seventh, synonym cycling, is absent because the material stages none — retry logic, backoff, and jitter are three things rather than three names for one.
  - `lens` — `pass` — no genre, no technique, no structural expectation, and no comment on the article's shape beyond the patterns.
  - `no-mechanics` — `pass` — `recieved` inside the exception message is not mentioned anywhere in the fifteen findings, and no mechanical pass appears in the trace.
  - `budget` — `pass` — `0` delegated nothing; the trace carries no subagent.
  - `language` — `pass` — `en_GB` inferred from *recognising*, verified against the installed resource.
  - `loading` — `pass` — the catalogue and the `en_GB` `anti-slop` scope, and nothing else. No tool call in the trace reads `base.md`, a genre, or a technique.
  - `target` — `pass` — no destination named, the response received the artifact.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — all fifteen.
- **defects filed** — #149.
- **notes** — three of the fifteen sit inside the code — the docstring, which the run reports as four patterns in one finding, and the two comments — and the run drew its own boundary within the block: *Repair the prose only — `retry`, `attempts`, `TransientError`, `ExhaustedError` and the message string are the program, not the text, and stay exactly as they are.* The correcting run below reached the opposite answer on the same material. Neither reading breaks a criterion here, and nothing in the Skill or in the correction brief settles which is right, so the disagreement is filed as #149 rather than judged.

#### `probe/code-slop-en.md` (two corrections, written to a file)

- **fixture** — none; run-local probe material
- **invocation** — `/unslop --max=2 --output=$RUN/out/code-post.md $RUN/probe/code-slop-en.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/code-post.md`
- **observed delivery** — the path, a line saying no findings remain, and a summary: ten findings, both correction rounds spent, and what the re-reading after the first round found.
- **side effects** — `out/code-post.md` created. Nothing else; the fixture itself is byte-identical afterwards.
- **criteria** —
  - `preserve` — `pass` — **this is the entry that carries the code half of the ticket's preservation criterion.** The run rewrote or cut the title and five paragraphs, so it is a run that genuinely changed the text; `diff` between the fixture and the delivered file has two hunks and twelve changed lines, every one of them prose, and the seventeen lines that are code come through as one identical run, `sha256` `aea186a9…` on both sides. The fenced Python block is byte-identical from ```` ```python ```` to ```` ``` ````, including the docstring, the comment, and the `recieved` misspelling in the exception message; the indented block is byte-identical, including its own *In conclusion, the key to success is randomness* comment and the *It is worth noting that* in its log format string; and both inline spans survive in a paragraph the run did edit, which lost its *Experts agree* clause and kept the spans exactly. `not_just_about()` and `STUDIES_SHOW` are named after two of the patterns the run was hunting and it renamed neither.
  - `lens` — `pass` — nothing outside the anti-slop lens was corrected. No genre, no technique, no structural expectation, and every changed line answers a finding the run named.
  - `no-mechanics` — `pass` — `recieved` is still misspelled in the delivered file, no mechanical pass appears in the trace, and the run says so itself: *mechanical correction is a separate gesture, and no mechanical pass ran.*
  - `detect` — `pass` — ten findings, across the same six patterns the review above reached; synonym cycling has nothing to find here either.
  - `budget` — `pass` — `2` given and `2` spent, as a ceiling reached rather than a quota filled: the second round exists because the re-reading found something, not because a unit was left.
  - `fresh` — `pass` — two subagents, each started fresh. Both prompts open *You have not seen this text before*, and each carries the complete current text and the complete current findings inline rather than by a path. The second carries the text as the first round left it.
  - `verify` — `pass` — the re-reading after round 1 found that stating the false contrast's second half on its own had left *Retry logic is about fundamentally rethinking how systems behave under pressure* standing as the opening — a new instance of a pattern the repair created. Round 2 removed it, and the re-reading after that came back clean.
  - `stop` — `pass` — the budget was spent and the last re-reading found nothing, so the run ended with no findings rather than with findings it had run out of budget for.
  - `language` — `pass` — `en_GB` by inference, no flag and no map in play.
  - `target` — `pass` — the artifact went to the named path, which did not exist and was created.
  - `effects` — `pass` — exactly one file appears in the inventory diff, at the path named, and nothing else changed.
- **unresolved findings** — none.
- **defects filed** — #149, shared with the review above; #150 for the corpus gap this material stands in for.
- **notes** — the ten findings are all outside the code, and the run gave its own reason for that opposite decision: *I treated code as verbatim material … the docstring and comments sit inside samples the text presents as source that ships in the real world.* Both runs left every byte of code alone, which is what `preserve` asks; what they disagree about is whether the prose inside a sample is a finding at all, which is #149.

### `slop-heavy` supplied inline — the control for #147

- **fixture** — `slop-heavy`, supplied inline rather than by path
- **invocation** — `/unslop ` followed by the whole of `prose/slop-heavy.md`, pasted inline as the operand
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a line saying one correction was spent and the result re-read, then the corrected text, then twenty findings summarised and six carried forward, three from the first pass and three found on the re-reading, each named by its pattern and located.
- **side effects** — none.
- **criteria** —
  - `lens` — `pass` — the whole flow ran and nothing outside it did.
  - `loading` — `pass` — `help.md`, the language list, the `en_GB` scope, the catalogue, `delivery.md`, `correction.md`; nothing wider.
  - `detect` — `pass` — twenty findings, all seven patterns.
  - `budget` — `pass` — the default of `1`, spent once.
  - `fresh` — `pass` — one subagent, started fresh.
  - `verify` — `pass` — three of the six carried-forward findings were found by the re-reading, two of them created by the repair: collapsing two anaphoric triples left two adjacent three-item lists.
  - `stop` — `pass` — budget spent with findings left.
  - `language` — `pass` — `en_GB` by inference from the pasted text.
  - `no-mechanics` — `pass` — none.
  - `target` — `pass` — response.
  - `effects` — `pass` — nothing written.
- **unresolved findings** — six.
- **defects filed** — none; this run is the control that #147 is filed against.
- **notes** — the corpus asks that inline supply be exercised at least once, and `brief-short` is the fixture it names for it. That run failed, and this one is why the failure is filed as *the artifact's own words look like a request* rather than as *inline supply is broken*: the same supply route, with prose instead of a brief, runs the Skill exactly as its steps describe.

### Refusals the corpus does not stage

Three of the invalid forms the Skill's DIAGNOSTICS section names have no fixture. Each was run once, on corpus material, against the same inventory as everything above.

- **fixture** — none; the material is corpus prose and the invocation is what is under test
- **invocation** — `/unslop --max=-1 $RUN/corpus/prose/slop-heavy.md`; `/unslop $RUN/corpus/prose/clean-en-GB.md $RUN/corpus/prose/flawed-sv.md`; `/unslop --output=$RUN/out/missing/dir/x.md $RUN/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — n/a; all three were refused
- **observed delivery** — three refusals, each naming the problem in one line, printing the SYNOPSIS verbatim, and pointing at `/unslop --help`. The Correction Budget one says `-1` is not a non-negative integer. The two-artifact one names both files and says the Skill reads exactly one text per invocation, then suggests two separate invocations. The destination one names the missing parent directory, says a run creates exactly one file at the named path and never a directory to hold it, and offers both the path that would work and the alternative of creating the directory first.
- **side effects** — none, in all three.
- **criteria** —
  - `refusal` — `pass` — all three name what was wrong, print the synopsis, point at help, and report that nothing was read and nothing written.
  - `effects` — `pass` — all three inventories are identical before and after; no file created, none truncated, no directory made.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — with `brief-article-abt` (undeclared flags), `url-source` (In-place Editing against a URL), `read-only-source`, `output-equals-source`, and `output-and-in-place` above, eight of the DIAGNOSTICS list's cases are on record and each of them left nothing behind.

## What this record establishes, and what it does not

Every fixture the corpus provides for this Skill was run. None was skipped, so no entry above carries a skip for that reason. Two criterion lines are `skipped` and each says why: `budget` on `brief-short`, where no correction loop ran because the run never reached one, and `stop` on the two quotation probes, which were staged for a condition they turned out not to reach and are recorded with the reason rather than removed. Of the 337 criterion lines in this record, 332 pass, three fail, and those two are skipped.

Three criterion lines failed, all three on one entry and all three for one cause, which is #147. The rest held: the patterns are caught in both supported languages, on Swedish instances and on ten of the Swedish scope's own items as well as on the shared catalogue's seven; clean fixtures come back with the short status rather than a rewritten text; a fixture's mechanical errors are still in it afterwards; no mechanical pass ran in any of the forty-nine traces; no genre, technique, or structural expectation entered any run, and two were refused when an invocation named them; the Correction Budget behaved as the loop contract specifies at `0`, at the default, and at `2` and `3`, with a fresh subagent per correction carrying the complete text and complete findings directly, a re-reading after each, and all three stopping conditions observed; language precedence held at each of its levels, and a recognized `kntnt` map supplied the language without being created, completed, synchronized, or otherwise disturbed, including on two runs that changed the text and one that wrote it to a file; frontmatter, formatting, code, and quotations came through untouched wherever the findings did not concern them, the code half on run-local material because the corpus stages none, and on a run that rewrote the title and five paragraphs around a fenced block it did not touch a byte of; no run remarked on source material it was not given; and the output contract was exercised through the real Skill seam across all ten behaviours the ticket lists, with no partial effect behind any refusal.

Three defects were found and filed rather than absorbed — #147, #148, and #149 — and one existing defect, #145, was extended to a second Skill. One gap in the corpus itself was found and filed as #150 rather than closed by adding to the corpus under the run that needed it. Nothing in the corpus, the protocol, or the criteria was changed to accommodate any of them.
