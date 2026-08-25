# write — claude — 2026-08-25

- **record** — `write-claude-2026-08-25`
- **date** — `2026-08-25`
- **ticket** — `#108`
- **skill** — `write`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.245
- **corpus commit** — `059e8bc`

## Run conditions

The Skill was run as a user of it runs it: `/write …` typed as the whole of a Claude Code turn, against the Skill as installed at `~/.agents/skills/write`, reached through `~/.claude/skills/write`, which symlinks to it. The installed Skill was byte-identical to `skills/editorial/write/` at the corpus commit, and the Collection Library it resolves through — `~/.agents/skills/kntnt/`, likewise symlinked — was byte-identical to `skills/kntnt/`. Neither identity was assumed: `diff -r` was run against both before the first run and reported no difference.

The Library did not begin that way. As found, the installed Manager was the Collection as it stood before the genres, the techniques, and the anti-slop catalogue were added, so `--genre=article` and `--technique=abt` named resources that were not there. That is what an author on this machine would have had, and it is not what this ticket evaluates: the corpus is run against the Collection at the corpus commit. The install was therefore brought up to it — the same files `/kntnt update` would have installed — with the previous state kept aside and put back when the runs were finished, so the machine ends as it began. The one run made before that was noticed is recorded under **Runs discarded** rather than kept.

Each fixture ran in its own turn with no memory of any other, and in its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says: `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/108.scratch/runs/<id>`; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form. **side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself.

Nothing in this repository was read by the runs, and no run was given the Skill's own instructions, the ticket, or the criteria below. Judging was done from the delivered reply and the filesystem inventory alone, fixture by fixture, before any GPT-family record existed to compare with. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

`/write` is unambiguous on this machine even though a legacy plugin, `kntnt-text-skills:write`, is installed beside the Collection's Skill. Every run below reached the Skill under evaluation with no routing hint, which is visible in each run's own account of what it loaded; the Proofread record's disambiguation sentence was not needed and was not used.

The criterion identifiers are stable across entries: `fidelity` (nothing in the draft that the material does not carry, and attribution, uncertainty, scope, chronology, and causality preserved), `quotation` (spoken quotations repaired only inside the boundary, and paraphrased where fidelity is doubtful), `language` (the draft is in the language the precedence names), `genre` (the resolved genre's contract is met and it is the one the precedence names), `technique` (a selected technique is complied with, and none is applied that was not selected), `register` (the baseline register, moved by genre, audience, and purpose where the fixture calls for it), `stops` (no review and no proofreading work, and neither offered as a next step of the run), `handoff` (the Kntnt map is attached or suppressed as the contract says, normalized, and merged rather than duplicated), `loading` (only the base contract, the selected genre, the composition scope, and an optional technique are read), `resolution` (each parameter settled at the level the precedence gives it), `ask` (a materially mixed language is asked about rather than guessed), `target` (the artifact went where the output contract sends it), `effects` (the filesystem shows what the contract allows and nothing else), and `refusal` (a refused invocation names the problem, prints the synopsis, points at help, and leaves nothing behind).

Two things about the criteria are worth a later reader's attention. `loading` counts `delivery.md` and `quotations.md` as inside the contract rather than beside it: the Skill's own steps send a run to the first before it settles a destination and to the second before it puts quotation marks around speech, so reading them is the instruction being followed. And the delivery contract's no-change status has no case here — Write creates a text rather than returning a changed version of one, so no run of it can finish with nothing to change. The nearest thing the corpus produces is a brief whose material cannot fill its stated length, and what those runs did with it is recorded on each of them.

## `brief-short` (inline material, response default)

- **fixture** — `brief-short`
- **invocation** — `/write ` followed by the fixture's complete text pasted in as inline material, as the corpus asks
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 403-word draft came back in the response with a `kntnt` map above it, followed by one paragraph saying what had been resolved and where the draft went; nothing was written.
- **side effects** — none under `$RUN`. The run wrote a copy of its own draft to `/tmp` to count its words and removed it in the same command; nothing was left behind there either.
- **criteria** —
  - `fidelity` — `fail` — an unsupported fact: *We were not trying to abolish meetings, and we had no theory about focus time* states the team's intent, and *separating a change in meetings from everything else that happened over the same three months is not something we know how to do honestly* supplies a reason for the non-measurement. The brief carries neither.
  - `genre` — `pass` — `general` was not taken by default but `article` was inferred from *a short piece for our engineering blog*, which is inference at its own step of the precedence, and the piece behaves as one throughout.
  - `technique` — `pass` — resolved as none and recorded as `none`.
  - `language` — `pass` — `en_GB`, the declared default for bare English, from the brief's own language.
  - `register` — `pass` — the baseline moved by the audience the brief names; plain, concrete, and not a news article.
  - `stops` — `pass` — no review and no proofreading, and neither offered.
  - `handoff` — `pass` — the map carries the three normalized values and nothing else.
  - `loading` — `pass` — `base.md`, `genres/article.md`, the `en_GB` composition scope, and `delivery.md`; no technique, no review half, no anti-slop, no other scope.
  - `target` — `pass` — no destination was named and the response received the draft.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #138.
- **notes** — the corpus's own floor for this fixture holds: no benefit is claimed anywhere, *nobody asked to go back* is delivered at the weight the brief gives it, and the unmeasured delivery speed is stated as unmeasured and given the closing position. What fails is the layer under that floor, and the same failure recurs on this fixture's other runs and on `brief-article-abt`; #138 is where it is written down.

## `brief-short` (new file)

- **fixture** — `new-file`
- **invocation** — `/write --output=$RUN/out/draft.md $RUN/corpus/source/brief-short.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/draft.md`
- **observed delivery** — the reply said the draft had been written to the named path, gave a table of what had been resolved and how, and did not repeat the text.
- **side effects** — `out/draft.md` created. Nothing else created, replaced, or removed; the brief is untouched.
- **criteria** —
  - `fidelity` — `fail` — an unsupported fact: *the few minutes before the reporting began* gives the informal chat a duration the brief does not.
  - `genre` — `pass` — `general`, and the draft behaves as a recognisable explanation throughout.
  - `technique` — `pass` — none, recorded as `none`.
  - `language` — `pass` — `en_GB`.
  - `handoff` — `pass` — the map is the file's leading frontmatter, with the three normalized values.
  - `loading` — `fail` — `genres/article.md` was read as well as the resolved `genres/general.md`, which is one genre resource more than the contract admits.
  - `target` — `pass` — exactly the named path was created, and the file holds the complete draft rather than the response holding it.
  - `effects` — `pass` — one file created, and it is the one named.
- **unresolved findings** — none.
- **defects filed** — #139.
- **notes** — reading the file supplied material and selected no destination; the destination came from the flag alone, which is the distinction the delivery contract draws.

## `brief-short` (existing file)

- **fixture** — `existing-file`
- **invocation** — `/write --output=$RUN/corpus/output/existing-target.md $RUN/corpus/source/brief-short.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — the reply reported the draft written and delivered, tabulated the resolution, and named the overwrite as authorised by the path itself.
- **side effects** — `corpus/output/existing-target.md` replaced. Nothing created beside it, and the brief is untouched.
- **criteria** —
  - `fidelity` — `fail` — an unsupported fact: *That is the arithmetic that decided it in the end* asserts what decided the change, and *the few minutes before anybody got round to their update* again gives the chat a duration.
  - `genre` — `pass` — `general`.
  - `language` — `pass` — `en_GB`.
  - `handoff` — `pass` — the map is the replacement file's leading frontmatter.
  - `loading` — `fail` — `genres/article.md` read beside the resolved `genres/general.md`.
  - `target` — `pass` — the occupant is gone and the exact named file holds the draft; no confirming flag was asked for and none was offered, which is what the contract says naming the path means.
  - `effects` — `pass` — exactly one file changed.
- **unresolved findings** — none.
- **defects filed** — #138, #139.
- **notes** — none.

## `brief-short` (existing directory)

- **fixture** — `existing-directory`
- **invocation** — `/write --output=$RUN/out $RUN/corpus/source/brief-short.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the file it had derived inside the directory and tabulated the resolution.
- **side effects** — `out/brief-short.md` created. Nothing else.
- **criteria** —
  - `fidelity` — `fail` — an unsupported fact: *We could have picked a number before we started — cycle time, review latency, something — and we did not* states a state of affairs behind the brief's *we have not measured*.
  - `genre` — `pass` — `general`.
  - `language` — `pass` — `en_GB`.
  - `loading` — `fail` — `genres/article.md` read beside the resolved `genres/general.md`.
  - `target` — `pass` — the name was derived from the source basename, kept the source's extension, and landed inside the named directory and nowhere else.
  - `effects` — `pass` — one file created in the directory that was named.
- **unresolved findings** — none.
- **defects filed** — #138, #139.
- **notes** — the draft's *four and a half hours of attention* is arithmetic on the brief's own forty-five minutes and six people, and the run said so; that is a derivation rather than a fact added, and is not what the `fidelity` line above rejects.

## `brief-short` (Handoff Metadata suppressed)

- **fixture** — `brief-short`
- **invocation** — `/write --frontmatter=no $RUN/corpus/source/brief-short.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 395-word draft in the response opening directly on its title, with no frontmatter of any kind, and a closing paragraph naming Handoff Metadata as off *as requested*.
- **side effects** — none.
- **criteria** —
  - `fidelity` — `fail` — an unsupported fact: *two people are missing five minutes that were never on the agenda in the first place* puts a number on a duration the brief does not give, and *the few minutes before anybody reached the first item* is the same invention earlier in the text.
  - `handoff` — `pass` — the `kntnt` map is absent, and nothing else was suppressed with it; the artifact needed no frontmatter of its own here, which is the case the next two entries cover.
  - `genre` — `pass` — `article`, inferred from the engineering blog the brief names.
  - `language` — `pass` — `en_GB`.
  - `stops` — `pass` — no review, no proofreading, neither offered.
  - `loading` — `pass` — `base.md`, `genres/article.md`, the composition scope, `delivery.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #138.
- **notes** — none.

## `brief-short` (genre that is not installed)

- **fixture** — `brief-short`
- **invocation** — `/write --genre=fiction $RUN/corpus/source/brief-short.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a one-line refusal naming `fiction` as no installed genre and listing the four that are, then the `SYNOPSIS` section verbatim, the pointer to `/write --help`, and a sentence saying nothing was written and nothing delivered.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named in one line, the synopsis is printed, help is pointed at, and the value is refused rather than falling back to the default.
  - `effects` — `pass` — the inventory is identical before and after; the brief was read and nothing else happened.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the installed set was read off the directory rather than recited from the help page, which is what makes the list in the refusal true of this installation.

## `brief-short` (read-only destination)

- **fixture** — `read-only-source`
- **invocation** — `/write --output=$RUN/corpus/output/readonly-source.md $RUN/corpus/source/brief-short.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/readonly-source.md`
- **observed delivery** — a refusal naming the destination as an existing read-only file and quoting its mode, then the synopsis and the help pointer, then a paragraph saying that no draft was composed, no file created or truncated, and the destination's permissions left alone — and that relaxing the read-only bit or diverting the draft elsewhere would each have substituted something for a refusal that had not been asked for.
- **side effects** — none. `corpus/output/readonly-source.md` is unchanged in content and in mode.
- **criteria** —
  - `refusal` — `pass` — the problem is named, the synopsis printed, help pointed at.
  - `effects` — `pass` — the inventory is identical before and after, the permission was not changed to make the write possible, and no substitute destination was invented.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus builds this fixture for an In-place Editing request, which Write does not offer under any spelling. What it exercises here is the other half of the same rejection: a destination the run cannot write, refused before anything is composed. The run had read `delivery.md` and nothing else when it stopped.

## `brief-article-abt`

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=article --technique=abt $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 660-word draft in the response with its `kntnt` map, followed by a note naming the resolution and describing the arc it had built; nothing was written.
- **side effects** — none.
- **criteria** —
  - `fidelity` — `fail` — an unsupported fact: *Every one of them had been opened*, asserted of the eleven December messages, and *Nobody triaged those messages as low priority. Nobody put them off*, an absence of decisions the brief does not record.
  - `genre` — `pass` — one angle, settled early and held; the material is at the surface; the two named people are in it with the roles the brief gives them; the title carries the angle rather than the subject.
  - `technique` — `pass` — the And is two years of an unassigned shared inbox, the But is that the visibility which makes the arrangement work is what makes ownership a guess, and the Therefore is per-agent assignment with a claimable queue. The relations hold and no connective is laid over a sequence.
  - `language` — `pass` — `en_GB`.
  - `quotation` — `pass` — Miriam Adler is in reported speech, not quotation marks, and the run said why: the brief paraphrases her rather than quoting her.
  - `register` — `pass` — trade-publication prose for readers who know the tools, and nothing is explained that the brief says they do not need explained.
  - `stops` — `pass` — no review, no proofreading, neither offered.
  - `handoff` — `pass` — `article`, `abt`, `en_GB`, normalized.
  - `loading` — `pass` — `base.md`, `genres/article.md`, `techniques/abt.md`, the composition scope, `delivery.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #138.
- **notes** — the corpus's floor holds in full: nothing is attributed to Miriam Adler that she is not given as saying, and both stated limits — a larger team, and no comparison with any other approach — are delivered rather than dropped. The two sentences the `fidelity` line names are circumstantial detail rather than the finding, which is exactly the form #138 is about.

## `brief-article-abt` (selectors normalized)

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=article --language=EN-gb --technique=ABT $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 673-word draft in the response, with the resolution named ahead of it and the normalization of both selectors called out.
- **side effects** — none.
- **criteria** —
  - `handoff` — `pass` — the map carries `language: en_GB` and `technique: abt`, not the spellings that were typed; a case and separator variant and an upper-case technique both reached the canonical value.
  - `fidelity` — `pass` — every figure and date is the brief's; the nine-week result is not written as a proven cause, the run says in the text that two agents describing a habit is not a measurement, and it warns that the December count and the nine-week maximum are not the same measure and that setting them side by side flatters the second. *The team is the same size, which rules out the most obvious rival explanation, though not every one of them* is the same claim the other runs over this brief overreached on, stated here at the strength the material supports.
  - `genre` — `pass` — one angle, held.
  - `technique` — `pass` — the arc holds and is not decoration.
  - `language` — `pass` — `en_GB`.
  - `quotation` — `pass` — Miriam Adler in reported speech, for the stated reason.
  - `loading` — `pass` — the base contract, the selected genre, the selected technique, the composition scope, `delivery.md`, and `quotations.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this run and the one above were given the same material and the same genre and technique, and they differ on `fidelity`. That is the variance #138 records: the careful reading is in the Skill's repertoire and is not reliably reached.

## `brief-article-abt` (Handoff Metadata merged with the artifact's own frontmatter)

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=article --output=$RUN/out/post.md $RUN/corpus/source/brief-article-abt.md -- The artifact is a Jekyll post for our blog and needs its own YAML frontmatter with title, layout: post, and date: 2026-08-25.`
- **contextual instruction** — `The artifact is a Jekyll post for our blog and needs its own YAML frontmatter with title, layout: post, and date: 2026-08-25.`
- **output target** — `$RUN/out/post.md`
- **observed delivery** — the reply reported the file written and said in as many words that the Jekyll frontmatter and the `kntnt` map share one block rather than two.
- **side effects** — `out/post.md` created. Nothing else.
- **criteria** —
  - `handoff` — `pass` — the file opens on one YAML block holding `title`, `layout`, `date`, and the `kntnt` map with its three normalized values; there is no second block, and no option or raw argument is embedded anywhere.
  - `technique` — `pass` — resolved as none and recorded as `none`, and the run said why in as many words: the source filename says `abt`, and a filename selects nothing.
  - `fidelity` — `fail` — an unsupported fact: the two agents are described as speaking *unprompted and independently of each other*, and the team is said to be *working the same hours, on the same volume of mail, which rules out … that the post-Christmas weeks were simply lighter*. The brief says only that the team is the same size.
  - `genre` — `pass` — `article`, from the invocation.
  - `language` — `pass` — `en_GB`.
  - `target` — `pass` — the named path was created and holds the complete artifact.
  - `effects` — `pass` — one file created.
- **unresolved findings** — none.
- **defects filed** — #138.
- **notes** — this is also the run that shows the Invocation Envelope's separator doing its work: everything after `--` was read as guidance about the artifact and none of it as formal input.

## `brief-article-abt` (Handoff Metadata suppressed, the artifact's own frontmatter kept)

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=article --frontmatter=no --output=$RUN/out/post.md $RUN/corpus/source/brief-article-abt.md -- The artifact is a Jekyll post for our blog and needs its own YAML frontmatter with title, layout: post, and date: 2026-08-25.`
- **contextual instruction** — `The artifact is a Jekyll post for our blog and needs its own YAML frontmatter with title, layout: post, and date: 2026-08-25.`
- **output target** — `$RUN/out/post.md`
- **observed delivery** — the reply reported the file written and stated that the `kntnt` map was suppressed while the Jekyll frontmatter the artifact needs was written as the artifact's own block.
- **side effects** — `out/post.md` created. Nothing else.
- **criteria** —
  - `handoff` — `pass` — the file's leading YAML holds `title`, `layout`, and `date` and no `kntnt` key. Turning the option off removed that map alone and not the frontmatter the artifact requires, which is the distinction this run exists to test.
  - `fidelity` — `fail` — an unsupported fact: the two agents are described as speaking *independently and without much embarrassment*, which the brief does not characterise.
  - `genre` — `pass` — `article`.
  - `technique` — `pass` — none, and again the run named the filename as selecting nothing.
  - `language` — `pass` — `en_GB`.
  - `target` — `pass` — the named path holds the complete artifact.
  - `effects` — `pass` — one file created.
- **unresolved findings** — none.
- **defects filed** — #138.
- **notes** — read against the entry above, the pair is the whole of the frontmatter option's behaviour on one artifact: one block with the map, one block without it, and the artifact's own keys unchanged either way.

## `brief-report-pac`

- **fixture** — `brief-report-pac`
- **invocation** — `/write --genre=report --technique=pac $RUN/corpus/source/brief-report-pac.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — an 805-word report in the response under named section headings, with its `kntnt` map, the resolution stated ahead of it, and a closing note naming which figures were arithmetic on the brief's own and which dates carried no year because the brief gives none.
- **side effects** — none.
- **criteria** —
  - `fidelity` — `pass` — every figure is the brief's or arithmetic on it, and the run said which; the counter-argument is not resolved by inventing evidence for or against it, which is the corpus's floor for this fixture. *Independence is asserted rather than established* and *a premium cannot be weighed against a risk nobody has sized* are the two things the material actually supports, and the report says both instead of settling the question.
  - `genre` — `pass` — the question is stated in the reader's terms and answered in the first paragraph; every figure carries what it counts and over what period; the on-call lead's objection is put at its strongest before it is answered; what the report cannot settle has a section of its own; the recommendation names the action, whose it is, by when, and what it saves; and the headings name what they hold.
  - `technique` — `pass` — the premise is falsifiable and stated early, the analysis tests it rather than accumulating confirmations, and the conclusion introduces nothing that was not weighed.
  - `language` — `pass` — `en_GB`.
  - `register` — `pass` — accountable rather than persuasive, with no arresting opening and no reach for significance at the end.
  - `stops` — `pass` — no review, no proofreading, neither offered.
  - `handoff` — `pass` — `report`, `pac`, `en_GB`.
  - `loading` — `pass` — `base.md`, `genres/report.md`, `techniques/pac.md`, the composition scope, `delivery.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run opened by saying it had cut one phrase of its own that outran the material before delivering. That is drafting, not a review pass: no other Skill was invoked and none was offered.

## `brief-press-release-sv` (language inferred)

- **fixture** — `brief-press-release-sv`
- **invocation** — `/write --genre=press-release $RUN/corpus/source/brief-press-release-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish press release of about 120 words in the response with its `kntnt` map, followed by three notes: that the material carries about half the news the brief's stated 350 words would need and that reaching it would have meant inventing, that Anna Lindqvist's remark is reported speech in the brief and so becomes attributed indirect speech rather than a quotation, and that the 6 May date carries no year because the brief gives none.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — Swedish, inferred from the material with nothing overriding it, and the whole reply is in the language it resolved for the text.
  - `fidelity` — `pass` — the two exclusions the brief states are in the release as its own sentence; nothing suggests the workshop repairs devices for visitors or sells parts; and no fact appears that the brief does not carry. The length was refused rather than padded, which is the behaviour #138 says is in the Skill's repertoire but not reliably reached.
  - `genre` — `pass` — the news, who, and when are the first sentence; the hours, the funding figure, the names and roles are in printable form; what the announcement excludes is said plainly and once; no quotation of enthusiasm is manufactured; and it ends with the contact the material gives.
  - `quotation` — `pass` — no quotation marks anywhere, and the run named the reason.
  - `technique` — `pass` — none.
  - `handoff` — `pass` — `press-release`, `none`, `sv`.
  - `loading` — `pass` — `base.md`, `genres/press-release.md`, the `sv` composition scope, `delivery.md`, and `quotations.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `brief-press-release-sv` (language named explicitly against the material)

- **fixture** — `brief-press-release-sv`
- **invocation** — `/write --genre=press-release --language=en_GB $RUN/corpus/source/brief-press-release-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — an English press release in the response with its `kntnt` map, preceded by a note that the material carries about half the news the stated length would need, and followed by two judgement calls: that the Swedish proper names stay as their holders spell them, and that *plan två* became *level two* rather than *the second floor* because the two floor-numbering conventions disagree and a journalist should be able to print it without checking.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — this is the fixture's own second case: a Swedish brief and an English draft, because the invocation said so. The flag beat the material, which is the top of the precedence beating the bottom of it.
  - `fidelity` — `pass` — the exclusions survive translation and are stated plainly; the funding figure, the hours, the date, and the contact are the brief's; nothing was added to reach the stated length, and the run said so.
  - `genre` — `pass` — news first, facts printable, exclusions said, contact last.
  - `register` — `pass` — information rather than selling, which the genre asks for and this material invites the opposite of.
  - `handoff` — `pass` — `press-release`, `none`, `en_GB`.
  - `loading` — `pass` — as the run above, with the `en_GB` composition scope.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the locale reached the mechanics of the text without any mechanics scope being loaded: the hours are *3pm to 7pm* and the amount is *180,000 kronor*, both British conventions, from composition guidance alone.

## `interview-transcript`

- **fixture** — `interview-transcript`
- **invocation** — `/write --genre=article Write a short trade-publication piece for workshop owners about what changed at Nordvik Verkstad when it started taking in electric vans. Quote Petra Halldin where the material supports it. The interview is at $RUN/corpus/source/interview-transcript.md. About 400 words.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 386-word article in the response with its `kntnt` map, and a closing note on three fidelity decisions: Jonas's remark paraphrased because Halldin prefixed it with *he said something like*, the lost weeks reported without a figure because she hedged it, and they/them used because the transcript gives no pronoun.
- **side effects** — none.
- **criteria** —
  - `quotation` — `pass` — every quotation in the draft is traceable to the transcript, with fillers, false starts, and searching repetition removed and nothing else. *It's not the engine. Everyone thinks it's the engine. It's the whole booking side of it* is the transcript's own sentence with *you know* and the doubled *the whole* taken out; *There were more that came in for a tyre change or something. That doesn't count, I wouldn't count that* keeps her double statement of the same refusal, which is her insisting rather than searching; *Do it first* and the warning about the date are verbatim. Nothing was added inside the marks, no hedge was removed, and no distinctive wording was smoothed into the surrounding register.
  - `fidelity` — `pass` — the self-correction survives as the substance it is: the article's first sentence says eleven vans *took a full service*, and the paragraph that carries the number says in as many words that Halldin counts only those and that tyre changes do not count. The corpus's floor — that quoting the bare *eleven* would be a misquotation and quoting a version that never existed would be worse — is met by carrying the corrected version and its correction together. The one causal claim, that a single charger turned a queue into a schedule, is the transcript's own.
  - `genre` — `pass` — one angle, people in it where the material has them, nothing explained that the audience knows.
  - `language` — `pass` — `en_GB`, and the run named the transcript's *tyre* as the evidence.
  - `technique` — `pass` — none.
  - `register` — `pass` — trade prose, and the quotations keep the speaker's voice rather than the article's.
  - `handoff` — `pass` — `article`, `none`, `en_GB`.
  - `loading` — `pass` — `base.md`, `genres/article.md`, the composition scope, `delivery.md`, and `quotations.md`, which the Skill's own step sends a run to before it quotes speech.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the pronoun decision is worth recording because the corpus index itself calls Halldin *her* and the transcript does not. The run noticed that the transcript gives no pronoun, chose the one that asserts nothing, and said it had. Whether Halldin has approved any of these quotations is outside what anything here verifies, and the draft claims nothing about it.

## `factual-source-long`

- **fixture** — `factual-source-long`
- **invocation** — `/write --genre=article Write an article of about 600 words for a regional newspaper about the line 4 trial, for readers who live in the area. The source is $RUN/corpus/source/factual-source-long.md and nothing else.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 629-word article in the response with its `kntnt` map, closing on a note that Salomonsson is paraphrased because the source reports what she said without giving her wording.
- **side effects** — none.
- **criteria** —
  - `fidelity` — `pass` — every one of the corpus's four rejections is avoided, and each is avoided by saying what the source says. The opening states in its second sentence that the municipality cannot say which of the three changes produced the result, because all three took effect on the same day. The seventeen April days are *left out* and *treated as missing rather than as zero*. The 71 per cent is delivered inside the survey's own caveat, with the 18 per cent response rate beside it and the reason non-respondents differ. No figure appears that is not in the source, and the estimate is labelled an estimate with the reason the source gives.
  - `genre` — `pass` — an angle a local reader has a stake in, the material at the surface, and a closing paragraph that is the limits rather than a summary.
  - `language` — `pass` — `en_GB`, and the run named the source's own *per cent*.
  - `technique` — `pass` — none.
  - `register` — `pass` — regional-newspaper prose; the numbers carry the piece and no adjective is asked to.
  - `stops` — `pass` — no review, no proofreading, neither offered.
  - `handoff` — `pass` — `article`, `none`, `en_GB`.
  - `loading` — `pass` — `base.md`, `genres/article.md`, the composition scope, `delivery.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the fixture built to catch a draft that turns a rich source into confident causation, and it is the one the run was most careful on. Read beside the `brief-short` runs, it says something about where the failure #138 records actually comes from: not from too much material, but from too little of it against a stated length.

## `url-source` (URL read, response default)

- **fixture** — `url-source`
- **invocation** — `/write ` followed by the brief the fixture carries, naming <https://www.rfc-editor.org/rfc/rfc2119.txt> as the source and nothing else
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 368-word explainer in the response with its `kntnt` map, and a note that the RFC was fetched raw rather than through a summarising fetch, so the definitions are the document's own.
- **side effects** — none.
- **criteria** —
  - `fidelity` — `pass` — no definition is attributed to the RFC that the RFC does not give, which is the corpus's floor here. MUST is *an absolute requirement*; SHOULD carries the RFC's own *valid reasons in particular circumstances* and the *full implications must be understood and carefully weighed*; MAY carries the interoperability obligation the RFC states as a MUST, which a bare reading of *optional* would lose. The authorship, the date, and the advice that documents say which RFC they follow are the document's.
  - `genre` — `pass` — `general`, and the piece is a recognisable explanation for the audience the brief names.
  - `language` — `pass` — `en_GB`.
  - `technique` — `pass` — none.
  - `loading` — `fail` — `genres/article.md` was read as well as the resolved `genres/general.md`.
  - `target` — `pass` — no destination was named and the response received the draft.
  - `effects` — `pass` — the inventory is identical before and after; a URL was read and nothing was written.
- **unresolved findings** — none.
- **defects filed** — #139.
- **notes** — the draft separates what RFC 2119 asks of a specification's author from what it asks of its reader, and says which is which. That is a distinction the source draws and a summariser would flatten; it is recorded because it is the sort of thing the criteria above would not otherwise catch either way.

## `url-source` (filename derived from the URL)

- **fixture** — `url-source`
- **invocation** — `/write --output=$RUN/out ` followed by the same brief
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the file it had derived inside the directory and said the name came from the referenced URL's title, there being no local source file to take a basename from.
- **side effects** — `out/key-words-for-use-in-rfcs-to-indicate-requirement-levels.md` created. Nothing else.
- **criteria** —
  - `target` — `pass` — the second of the delivery contract's three name sources was used because the first was not available, the name is the RFC's own title reduced to something a filesystem accepts, it kept a suitable text extension, and it landed inside the named directory.
  - `fidelity` — `pass` — as the run above; the run also named two things it had left out of the artifact for length, both of them omissions rather than additions.
  - `genre` — `pass` — `general`.
  - `language` — `pass` — `en_GB`.
  - `loading` — `fail` — `genres/article.md` read beside the resolved `genres/general.md`.
  - `effects` — `pass` — one file created, in the directory that was named.
- **unresolved findings** — none.
- **defects filed** — #139.
- **notes** — none.

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/write Turn $RUN/corpus/prose/resembles-abt.md into a short piece for our engineering blog, about 300 words, for other small teams.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 318-word piece in the response with its `kntnt` map, and a closing paragraph saying in as many words that the source is called `resembles-abt.md`, that its three paragraphs do fall into an and-but-therefore shape, and that no technique was applied because none was selected.
- **side effects** — none.
- **criteria** —
  - `technique` — `pass` — this is the fixture's whole point and it holds at every place it could have failed: nothing was reported as resolved, the map records `technique: none`, and the draft is built on a different spine from the source's. The source even opens its third paragraph with *Therefore*, and that did not select anything either.
  - `fidelity` — `fail` — an unsupported fact: *It was the traffic somebody else began sending, on a day nobody told us about*. The source says the reading-list tool began linking in March and that nobody noticed for eleven days; that nobody was told is not in it.
  - `genre` — `pass` — `article`, inferred from the engineering blog.
  - `language` — `pass` — `en_GB`.
  - `loading` — `pass` — `base.md`, `genres/article.md`, the composition scope, `delivery.md`; `techniques/abt.md` was not read, which is the loading half of the same result.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #138.
- **notes** — the draft's closing advice and its reading of what the missing alerting means are the writer's own argument rather than reported fact, and are not what the `fidelity` line rejects; the sentence named there is.

## `mixed-language` (nothing named)

- **fixture** — `mixed-language`
- **invocation** — `/write Turn the retrospective notes at $RUN/corpus/prose/mixed-language.md into a short summary for the team, about 200 words.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no draft. The reply said the language had to be settled first, quoted a sentence from the notes that switches language twice inside itself, said that the brief is English and the source mixed so neither settles it, listed the three installed candidates with what each would follow from, and asked which. It then said that everything else was settled and needed nothing — genre `general`, no technique, the response, the map attached — and stopped.
- **side effects** — none.
- **criteria** —
  - `ask` — `pass` — the corpus's floor is that a language must not be silently picked and acted on, and nothing was picked and nothing was acted on. The candidates were named, as the Skill's own resolution step says they should be.
  - `resolution` — `pass` — the ambiguity stopped one parameter and not the rest; the other four were resolved and reported.
  - `loading` — `pass` — no contract was loaded at all, the run having stopped before the step that loads it.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run listed `en_US` among the candidates as well as `en_GB` and `sv`, which is the honest list: nothing in the material settles the English variant either.

## `mixed-language` (language named)

- **fixture** — `mixed-language`
- **invocation** — `/write --language=sv Turn the retrospective notes at $RUN/corpus/prose/mixed-language.md into a short summary for the team, about 200 words.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 138-word Swedish summary in the response with its `kntnt` map, prefaced by a sentence saying that the notes mix the two languages clause by clause but that the flag had settled it so there was nothing to ask about, and closed by a note that 200 words would have meant padding and what further material would close the gap.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — Swedish, from the invocation, over material that no inference could have settled. Read beside the run above, the pair is the difference the precedence makes: the same material asks a question without the flag and none with it.
  - `fidelity` — `pass` — the blocker, the two conclusions, the three action points, and both names are the notes'; nothing was added to reach the stated length, and the run said so.
  - `genre` — `pass` — `general`, and the run named why no installed genre fits a short internal note.
  - `technique` — `pass` — none.
  - `handoff` — `pass` — `general`, `none`, `sv`.
  - `loading` — `fail` — `genres/report.md` was read as well as the resolved `genres/general.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #139.
- **notes** — the Swedish is idiomatic rather than translated: V2 order throughout, compounds written as one word, and the closing *Och vi startar ingen backfill på en fredag* keeping the notes' own English loanword rather than hunting it down. That is the composition scope reaching the text.

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/write Write a follow-up piece of about 400 words, for the same readers, building on $RUN/corpus/frontmatter/handoff-present.md and the question it leaves open.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 400-word article in the response with its own `kntnt` map, opening on a line naming all three values as taken from the material's map.
- **side effects** — none. The source file is untouched.
- **criteria** —
  - `resolution` — `pass` — nothing was named on the invocation and all three fell through to the map, which is the fixture's whole case. The values were reported back in the spellings the map carries.
  - `genre` — `pass` — `article`, from the map, and the draft is one.
  - `technique` — `pass` — `abt`, from the map, and the arc holds: the falling storage price as what made selection unnecessary, 2023 as what removed it, and an unowned decision as what follows.
  - `language` — `pass` — `en_GB`, from the map.
  - `fidelity` — `pass` — the 2011 approval, the 2023 pair of changes, the forty times, the 60 per cent, and the 9,000 items a year are the source's, and the draft's argument about what they mean is visibly its own rather than reported.
  - `handoff` — `pass` — the delivered artifact carries the same three values.
  - `loading` — `pass` — `base.md`, `genres/article.md`, `techniques/abt.md`, the composition scope, `delivery.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/write --genre=article --language=sv Skriv en text på ungefär 400 ord som bygger vidare på $RUN/corpus/frontmatter/handoff-conflicting.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a Swedish article of about 390 words in the response with its `kntnt` map, opening on a line saying that genre and language came from the invocation, that the map's `report` and `en_US` were suppressed by it, and that the technique came from the map.
- **side effects** — none. The source file is untouched.
- **criteria** —
  - `resolution` — `pass` — every one of the corpus's three rejections is avoided. No metadata value overrode an explicit one; the two explicit values suppressed the map for their own parameters and not for the third; and the delivered artifact's map is the configuration the run actually resolved rather than the one the source carried.
  - `genre` — `pass` — `article`, from the invocation over the map's `report`.
  - `language` — `pass` — `sv`, from the invocation over the map's `en_US`, and over a Swedish body that would have inferred the same.
  - `technique` — `pass` — `pac`, from the map because nothing higher named one, and the arc holds: what the thirty-five minutes measures as the premise, three objections and one supporting point as the analysis, and what stands after them as the conclusion.
  - `fidelity` — `pass` — the four hours, the thirty-five minutes, the 3 February date, the unchanged old queue, and both of the source's own unknowns are carried; *nästan sju gånger snabbare* is arithmetic on the two figures, and the observation that a median says nothing about its own tail is about what a median is rather than about this case.
  - `handoff` — `pass` — `article`, `pac`, `sv`, normalized.
  - `loading` — `pass` — `base.md`, `genres/article.md`, `techniques/pac.md`, the `sv` composition scope, `delivery.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the run that shows per-parameter precedence rather than per-invocation precedence, which is the thing the specification is most specific about and the easiest to implement wrongly.

## `handoff-unusable`

- **fixture** — `handoff-unusable`
- **invocation** — `/write Write a short follow-up of about 300 words building on $RUN/corpus/frontmatter/handoff-unusable.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no draft. The reply said it had stopped before writing anything, quoted the map, said that `article` and `abt` both resolve and `en_UK` does not, quoted the resolver's own diagnostic naming the three installed languages, and explained that the invocation carried no `--language` so the map was the deciding level for that parameter. It then offered the two ways forward — settle it on the invocation, or correct the file — and stopped.
- **side effects** — none. The source file is untouched.
- **criteria** —
  - `resolution` — `pass` — both of the corpus's rejections are avoided: `en_UK` was not read as `en_GB`, and the run did not continue as though the metadata had been usable. It also did not fall through to inferring the language from the material's own English prose, and said in as many words why not — a map is a recorded decision rather than a hint, and either substitution would overwrite a decision the user cannot see being made.
  - `refusal` — `pass` — unusable artifact metadata was reported as such rather than taking the syntax refusal, which is the distinction the specification draws; no synopsis was printed, correctly, the invocation's own form being valid.
  - `loading` — `pass` — nothing was loaded; the run stopped before the step that loads.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the diagnostic the run quoted is the resolver's, not the Skill's paraphrase of it, so the list of installed languages in the reply is true of this installation rather than of the help page.

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/write Write a short follow-up of about 300 words building on $RUN/corpus/frontmatter/frontmatter-unrelated.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 291-word piece in the response with its own `kntnt` map, opening on a sentence naming all four bait keys and saying that ordinary document frontmatter carries no configuration whatever its keys are called.
- **side effects** — none. The source file is untouched, frontmatter included.
- **criteria** —
  - `resolution` — `pass` — `genre: fiction`, `technique: montage`, `language: Esperanto`, and `lang: fr` were each named and each read as document frontmatter rather than as configuration, which is the corpus's floor. Every parameter fell through to the level below.
  - `genre` — `pass` — `general`, the default, reached because nothing above it applied.
  - `technique` — `pass` — none, and `montage` names nothing installed in any case.
  - `language` — `pass` — `en_GB`, inferred from the brief and the material's own prose rather than from `lang: fr` or `language: Esperanto`.
  - `handoff` — `pass` — the new artifact carries the resolved values; the source's frontmatter was neither read as this collection's nor changed.
  - `loading` — `pass` — `base.md`, `genres/general.md`, the composition scope.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is a Skill that creates a text rather than returning a changed one, so the corpus's second rejection — a change to the frontmatter block — is met by the source not being written to at all.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/write Write a short follow-up of about 300 words building on $RUN/corpus/frontmatter/frontmatter-absent.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a 299-word piece in the response with its `kntnt` map, opening on a line saying the source carries no frontmatter so nothing was read from it as configuration. A closing message said the scratch file it had used for counting words was removed.
- **side effects** — none under `$RUN`; the `/tmp` scratch file the run made for counting was removed by the run itself.
- **criteria** —
  - `resolution` — `pass` — no metadata was demanded, nothing was refused, and every parameter resolved at a lower level.
  - `handoff` — `pass` — the new artifact carries a map because the option is on by default; nothing was added to the source, which is the corpus's own rejection here.
  - `genre` — `pass` — `general`.
  - `language` — `pass` — `en_GB`, and the run named the source's *artefact* and *rota* as settling the variant.
  - `fidelity` — `pass` — the source is an argument rather than a report, and the follow-up argues from it without asserting anything about a case. Its *costs four seconds* is a figure of speech in the writer's own voice rather than a quantity attributed to a reported event, which is where this record draws the line.
  - `loading` — `fail` — `genres/article.md` was read as well as the resolved `genres/general.md`.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #139.
- **notes** — none.

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/write --output=$RUN/corpus/output/collision Turn the notes at $RUN/corpus/output/interview-notes.md into a short piece of about 250 words for a trade publication.`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the reply named the file it had written, said the stem came from the source basename, that both `interview-notes.md` and `interview-notes-2.md` were occupied, that the first free numbered candidate was taken, and that neither occupant was touched.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants are byte-identical to the corpus, and the source notes are untouched.
- **criteria** —
  - `target` — `pass` — both of the corpus's rejections are avoided: neither occupant was overwritten, and the name was built by suffixing the original stem rather than the colliding candidate, so the sequence is `interview-notes`, `-2`, `-3` and not `interview-notes-2-2.md`.
  - `fidelity` — `pass` — nothing appears that the notes do not carry. The run named two inferences of its own before making them — that Halldin is given no role in the notes, and that the vans are electric, which the high-voltage course and the charger make plain but the notes never state — and left the reader to overrule either.
  - `quotation` — `pass` — no quotation marks anywhere, because the notes are a summary of what Halldin said rather than her words; the closing line about *probably* is attributed paraphrase. That is the second of `quotations.md`'s cases for paraphrasing, correctly identified.
  - `genre` — `pass` — `article`, inferred from the trade publication the request names.
  - `language` — `pass` — `en_GB`.
  - `effects` — `pass` — one file created, and it is the one the derivation named.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the draft is 222 words against a stated 250, and the run said the notes hold no further material it could add without inventing. That is the same judgement the two press-release runs made, and its absence on `brief-short` and `brief-article-abt` is #138.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/write --output=$RUN/corpus/output/in-place-source.md Rework the text at $RUN/corpus/output/in-place-source.md into a shorter piece of about 200 words.`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/in-place-source.md`
- **observed delivery** — a refusal saying that `--output` names the same local file the brief supplies as material, that this Skill creates a text and never overwrites its own source, then the synopsis, the help pointer, and a sentence saying nothing was written and the file untouched, with a suggestion of what would work instead.
- **side effects** — none. `corpus/output/in-place-source.md` is byte-identical to the corpus.
- **criteria** —
  - `refusal` — `pass` — the problem is named in one line, the synopsis is printed verbatim, help is pointed at, and the refusal comes before anything is composed.
  - `effects` — `pass` — the inventory is identical before and after; the corpus's own rejection is that the file is replaced, and it is not.
  - `loading` — `pass` — nothing was loaded.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the delivery contract points such a refusal at In-place Editing, which for Write is a gesture that does not exist; the refusal here says instead that this Skill has no such destination and names a different path as the way forward, which is the same instruction under a Skill that creates rather than changes a text.

## `in-place-request`

- **fixture** — `in-place-request`
- **invocation** — `/write --in-place=yes Rework the text at $RUN/corpus/output/in-place-source.md into a shorter piece of about 200 words.`
- **contextual instruction** — `none`
- **output target** — none named
- **observed delivery** — a refusal saying `--in-place=yes` is not one of this Skill's options and that an unknown option is refused rather than ignored, then the synopsis and the help pointer, then a sentence saying nothing was read, nothing written, and no draft produced, and a note that in-place editing is not offered under any spelling because this Skill creates a text.
- **side effects** — none. The file the invocation named is byte-identical to the corpus.
- **criteria** —
  - `refusal` — `pass` — the unknown option is refused rather than ignored, which is the rule the Skill states about flags with no work to do.
  - `effects` — `pass` — the inventory is identical before and after, and the source was not replaced.
  - `loading` — `pass` — nothing was loaded; the run refused on the form.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus builds this fixture for a Skill that offers In-place Editing. Write does not, and what the fixture exercises here is that the gesture is absent rather than silently accepted — the corpus's own rejection, the source replaced without an explicit request, could not be nearer.

## `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/write --output=$RUN/out/draft.md --in-place=yes Rework the text at $RUN/corpus/output/in-place-source.md into a shorter piece of about 200 words.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/draft.md` and In-place Editing, at once
- **observed delivery** — a refusal on the unknown option, the synopsis, the help pointer, and a sentence saying that `out/draft.md` was not created, followed by the invocation with the flag dropped as the thing that would work.
- **side effects** — none. `out/` is empty and the named source is byte-identical to the corpus.
- **criteria** —
  - `refusal` — `pass` — the contradictory half was refused before the valid half executed, which is what the delivery contract asks of a contradictory request.
  - `effects` — `pass` — neither half executed: no file was created at the named path, and the source was not replaced. The inventory is identical before and after.
  - `loading` — `pass` — nothing was loaded.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the two are mutually exclusive by the delivery contract and, in this Skill, one of them does not exist; either way the corpus's rejection is that half of it executes, and neither did.

## `response-default`

- **fixture** — `response-default`
- **invocation** — every run above that named no destination; the fixture is a situation rather than material
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete draft in the response in each case, with no file created anywhere.
- **side effects** — none, in every one of the twenty-one runs that named no `--output`. Each of their inventories is identical before and after.
- **criteria** —
  - `target` — `pass` — the default held whether the material was inline, a local file, or a URL; reading a file selected no destination in any run.
  - `effects` — `pass` — the corpus's rejection here is any file created, replaced, or removed under `$WORK` by a run that named no destination, and no such run touched anything under `$WORK`.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — nine of these runs made a scratch copy of their own draft under `/tmp` to count its words and removed it in the same command; none survived the run, none was under `$WORK`, and none was the artifact. It is recorded because a later reader checking only `$WORK` would not see that the system temp directory was touched at all.

## `<no brief>`

- **fixture** — none; the invocation is the case
- **invocation** — `/write`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a one-line refusal saying the invocation carries no brief, points at no material, and has no applicable guidance in context to supply one, then the synopsis verbatim and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the case the Skill names as *nothing to write* is refused as such rather than answered with a draft about nothing.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus has no fixture for this because it is a property of the invocation rather than of any material; it is recorded here because the acceptance criteria ask that a refusal leave no partial effect, and an empty invocation is the cheapest place to see that.

## Fixtures deliberately skipped

Five fixtures were not run against this Skill. Each is recorded here rather than omitted, because a record silently missing a fixture reads later as a fixture that passed.

- `clean-en-GB` — `skipped` — the fixture for a mechanical pass that should find nothing and a review that should not rewrite competent prose. Write performs neither pass, and its `Reject` line judges changes to a supplied text, which this Skill does not make: it creates a new artifact and leaves its material alone, which every entry above records from the filesystem.
- `flawed-en-US` — `skipped` — the main fixture for complete mechanical correction and for the boundary between correcting and rewriting. Write loads no mechanics scope by contract and corrects nothing; its `Reject` line has nothing here to reject.
- `flawed-sv` — `skipped` — same reason. The part of it that could bear on this Skill is whether Swedish reaches the text at all, and that is exercised by `brief-press-release-sv` and by `mixed-language` under `--language=sv`, both of which came back in idiomatic Swedish.
- `slop-heavy` — `skipped` — the fixture for anti-slop review. Write loads no anti-slop catalogue, produces no findings, and its `Reject` line judges a review's findings and a correction's damage, neither of which exists in a Write run.
- `locale-divergent` — `skipped` — its `Reject` line judges whether the resolved locale reaches a mechanical pass, and mechanics are the one scope Write never loads. The locale reaching a draft is exercised instead by `brief-press-release-sv` under `--language=en_GB`, where the composition scope alone produced British hours and a British thousands separator.

## Runs discarded

One run is named here so that the count of turns spent is honest, and it carries no criteria: it says nothing about this Skill.

The first attempt at `brief-article-abt` was made before the installed Collection Library was noticed to be older than the corpus commit. It refused `--genre=article` and `--technique=abt` as naming resources that are not installed, which was true of the Library it was reading and false of the Collection this ticket evaluates. It is discarded rather than recorded, and the fixture was re-run from a fresh working copy against the Library at the corpus commit; it is that re-run this record holds. The refusal itself was correct in form — it named the problem, printed the synopsis, wrote nothing, and declined to read a genre out of an unrelated plugin's directory that happened to have one — which is why the run is worth a paragraph even though it is worth no criteria.
