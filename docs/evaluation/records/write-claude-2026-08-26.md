# write — claude — 2026-08-26

- **record** — `write-claude-2026-08-26`
- **date** — `2026-08-26`
- **ticket** — `#158`
- **skill** — `write`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.246
- **corpus commit** — `46ba9c1`

## Run conditions

The Skill was run against the copy installed at `~/.claude/skills/write`. `diff -r` reported that directory byte-identical to `skills/editorial/write/` at the corpus commit, and the same for `~/.claude/skills/kntnt/` against `skills/kntnt/` — the Manager and the Collection Library it resolves language selectors and its delivery contract through — with no difference but the untracked `__pycache__` directories the repository working tree carries and an installed copy does not. Write declares no peer Skill, so the Manager and its Library are the whole of its dependencies.

Each fixture ran in a Claude Code agent session of its own, started from this session, with no memory of any other run and no access to this repository's evaluation material: the turn carried the invocation and nothing else, and no run was given the ticket or the criteria below. Each ran in its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says — `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form.

**side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself. Where a run delivered to a file, the file on disk is what was judged.

**What the inventory covered, and what it did not.** The inventory above is taken over the staged copy of the corpus and nothing else, so a file written outside it would not have appeared in any entry's **side effects**. That turned out to matter, and it is why this paragraph exists: at the end of the session the Harness's own scratchpad directory held exactly one file no run of this evaluation had been asked to create. It came from Write, and the correction it forced is recorded on the `brief-short (inline material, response default)` entry below and filed as #180. The same check found nothing left by any run of the other three Skills.

**How the Skill was started, and why it is worth saying.** Write carries `disable-model-invocation: true`, which is the point of it — the Skill is reserved for a user typing `/write`. That flag also means the Skill tool refuses to start it from inside a turn, and a sub-session receives a prompt rather than an expanded slash command. Sixteen runs were driven that way first and every one of them was refused, correctly and for the same stated reason; they are recorded under **Runs discarded** and carry no criteria.

What each run below was given instead is what the Harness itself gives a user-invoked Skill: its own instructions. The turn named `/Users/thomas/.claude/skills/write/SKILL.md` as the turn's instructions and `$HERE` as the directory holding it, and the run read that file from disk and followed it — including the checker it runs, the resolver it runs, and every reference it loads. The Collection's own vocabulary is what makes this the same seam rather than an imitation of one: a user-invoked Skill's body *is* static instructions, not a preprocessed template, so a turn carrying those instructions is the turn a user's slash command produces. Nothing was paraphrased, summarised, or supplied out of band; the bytes came from the installed Skill, and a run that read past what the Skill told it to read would be visible in its own account of what it loaded.

Judging was done from the delivered reply and the filesystem inventory alone, against the criteria below, fixture by fixture, before any GPT-family record existed to compare with. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

The criterion identifiers are stable across entries: `fidelity` (nothing in the draft that the material does not carry, and attribution, uncertainty, scope, chronology, and causality preserved), `quotation` (spoken quotations repaired only inside the boundary, and paraphrased where fidelity is doubtful), `language` (the draft is in the language the precedence names), `genre` (the resolved genre's contract is met and it is the one the precedence names), `technique` (a selected technique is complied with, and none is applied that was not selected), `register` (the baseline register, moved by genre, audience, and purpose where the fixture calls for it), `stops` (no review and no proofreading work, and neither offered as a next step of the run), `handoff` (the Kntnt map is attached or suppressed as the contract says, normalized, and merged rather than duplicated), `loading` (only the base contract, the selected genre, the composition scope, and an optional technique are read), `resolution` (each parameter settled at the level the precedence gives it), `ask` (a materially mixed language is asked about rather than guessed), `target` (the artifact went where the output contract sends it), `effects` (the filesystem shows what the contract allows and nothing else), and `refusal` (a refused invocation names the problem, prints the synopsis, points at help, and leaves nothing behind).

As in the record this one follows, `loading` counts `delivery.md` and `quotations.md` as inside the contract rather than beside it: the Skill's own steps send a run to the first before it settles a destination and to the second before it puts quotation marks around speech, so reading them is the instruction being followed.

## `brief-short` (inline material, response default)

- **fixture** — `brief-short`
- **invocation** — `/write <the brief's text, pasted inline>`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete draft in the response, frontmatter and all, followed by the resolved configuration, the length against the material, three things that would close the gap, and two judgement calls flagged for the user's eye.
- **side effects** — `draft.md` created in the Harness's scratchpad directory, holding the complete delivered draft. Nothing under the staged copy of the corpus.
- **criteria** —
  - `fidelity` — `pass` — the brief's six facts and no seventh. *We have not measured whether anything shipped faster* is not merely kept but argued: the draft says it will not imply otherwise, and gives the reason — three months in a six-person team cannot tell a process change apart from everything else in those three months. *Nobody asked to go back* is reported and then weakened in the same breath, on the ground that people seldom campaign to reinstate a meeting, which is the draft declining to let a fact carry more than it can.
  - `genre` — `pass` — `general` inferred, named as the contract a blog post is written against.
  - `technique` — `pass` — none selected, none applied.
  - `language` — `pass` — `en_GB`, and the reply reports what the composition scope did with it.
  - `register` — `pass` — written for other small teams, with the cost placed before the benefit; the reply flags that ordering as a choice rather than making it silently.
  - `handoff` — `pass` — a `kntnt` map with `general`, `none`, `en_GB`.
  - `stops` — `pass` — no review or proofreading, and neither offered as a next step.
  - `target` — `fail` — **an incorrect side effect.** The draft came back in the response, and a complete copy of it was also written to `draft.md` in the Harness's scratchpad directory. Nothing in the turn named a destination; the second run's turn carried no filesystem path at all, so the location came from the Harness's standing instruction to use its scratchpad for working files rather than from the user. The delivery contract is unconditional — a run that keeps the default *creates no file, touches no file, and makes no directory*.
  - `effects` — `fail` — the same finding, and the worse half of it: the reply says *output to this response, so nothing was written to disk* while the file is on disk. A caller reading that account has no way to learn that a copy of their text exists somewhere they did not ask for it.
- **unresolved findings** — three gaps in the material, and the four-and-a-half-hours arithmetic flagged as derived rather than supplied.
- **defects filed** — #180.
- **notes** — this is the fixture's inline-supply case: the brief was pasted into the invocation rather than named as a file, which is the one thing the corpus asks be exercised at least once. The two failures above were found after the rest of this record was written, during the session's own cleanup, and then reproduced: a second run of the same invocation from a fresh working copy wrote the same file, was watched from outside, and left it there. The file survived the run rather than being removed, so it is not a scratch buffer tidied away — several runs of the sibling Skills in this evaluation did report removing theirs. An earlier run of this invocation is recorded under **Runs discarded** for a different reason, and what it wrote is now readable as the same behaviour rather than as the harness sentence it carried.

## `brief-short` (new file)

- **fixture** — `brief-short`
- **invocation** — `/write --output=$RUN/out/status-meeting.md <the brief's text, pasted inline>`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/status-meeting.md`
- **observed delivery** — the reply named the path, named the resolved configuration, gave the angle in a sentence, and listed four things the material does not carry; the draft was not repeated.
- **side effects** — `out/status-meeting.md` created. Nothing else.
- **criteria** —
  - `fidelity` — `pass` — every claim in the file traces to the brief. The forty-five minutes, the six people, the Monday deadline, the Thursday call, the two of six, and *nobody asked to go back* are all there; *We have not measured whether anything shipped faster* is not merely kept but made the title's promise — *We dropped our weekly status meeting, and we cannot tell you it made us faster*. The one derived figure, four and a half hours, is arithmetic on the brief's own numbers and is presented as such.
  - `genre` — `pass` — `article` inferred, and the reply names the inference and the four installed genres it was made against.
  - `technique` — `pass` — none applied, and the reply says a technique is never inferred.
  - `language` — `pass` — `en_GB` from the language of the brief.
  - `register` — `pass` — a trade-blog register for other small teams; no advocacy, and the one claim that would sell the decision is explicitly withheld.
  - `handoff` — `pass` — the file opens on a `kntnt` map carrying `genre: article`, `technique: none`, `language: en_GB` and nothing else, with `none` where no technique was resolved.
  - `stops` — `pass` — the reply says in as many words that it has not reviewed or proofread the draft and that those are separate invocations.
  - `target` — `pass` — exactly the named file was created, and the draft did not also appear in the response.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — the four gaps in the material, reported with the artifact.
- **defects filed** — none.
- **notes** — the run reports removing two sentences on a self-check that had asserted an intent and an absence the brief does not record. That is the invariant catching itself before delivery rather than after.

## `brief-short` (existing file)

- **fixture** — `brief-short`
- **invocation** — `/write --output=$RUN/corpus/output/existing-target.md <the brief's text, pasted inline>`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — the reply said the file already there had been overwritten, named the resolved configuration, and listed three things that would close the length gap; the draft was not repeated.
- **side effects** — `corpus/output/existing-target.md` replaced. Nothing else.
- **criteria** —
  - `fidelity` — `pass` — the same set of facts and the same refusal to claim a net time saving; the reply distinguishes what the brief supports (the meeting's attention is gone) from what it does not (that the team came out ahead).
  - `genre` — `pass` — `general` inferred here rather than `article`, which is a different reading of the same brief and a defensible one; the reply names it and why.
  - `handoff` — `pass` — a `kntnt` map with the three normalized values.
  - `target` — `pass` — the occupant was replaced, no second confirming gesture was asked for, and nothing was written beside it.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
- **unresolved findings** — three gaps in the material, reported with the artifact.
- **defects filed** — none.
- **notes** — `general` here against `article` in the entry above is genre inference landing differently on one brief. Both are inferences the precedence permits at its fifth level, both were named in the reply, and neither draft reads as the other genre, so this is not a criterion failure; it is what an inferred parameter looks like.

## `brief-short` (existing directory)

- **fixture** — `brief-short`
- **invocation** — `/write --output=$RUN/out <the brief's text, pasted inline>`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the derived filename, said the output path had named an existing directory and that nothing else in it was touched, and listed the material that would close the length gap.
- **side effects** — `out/we-replaced-our-weekly-status-meeting-with-a-written-update.md` created. Nothing else.
- **criteria** —
  - `target` — `pass` — the material was inline, so there was no source basename and no URL title to derive from; the name came from the Skill's own working title, which is the third of the three sources the delivery contract names, and it kept a suitable text extension.
  - `fidelity` — `pass` — seven facts named and used; the reply flags the two things in the draft that are derived rather than stated — the four and a half hours, and the choice to frame the piece as a report rather than a recommendation.
  - `genre` — `pass` — `general` inferred, with the reasoning given against `article` explicitly.
  - `handoff` — `pass` — the map is attached.
  - `effects` — `pass` — one file created inside the named directory, nothing outside it.
- **unresolved findings** — the length shortfall and the material that would close it.
- **defects filed** — none.
- **notes** — none.

## `brief-short` (Handoff Metadata suppressed)

- **fixture** — `brief-short`
- **invocation** — `/write --frontmatter=no --output=$RUN/out/no-frontmatter.md <the brief's text, pasted inline>`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/no-frontmatter.md`
- **observed delivery** — the reply named the path, said the file carries no `kntnt` map and that nothing else about the artifact required frontmatter, and reported the length against the material.
- **side effects** — `out/no-frontmatter.md` created. Nothing else.
- **criteria** —
  - `handoff` — `pass` — the file begins on its `#` heading with no leading YAML at all, which is right for an artifact that needed none of its own.
  - `fidelity` — `pass` — the reply separates the brief's facts from the draft's reasoning about the format, and says explicitly that the paragraph arguing for writing over speech is reasoning rather than a claim about the team.
  - `genre` — `pass` — `general`, named as the default and as the contract a blog post is written against.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — the length shortfall and four named gaps.
- **defects filed** — none.
- **notes** — this entry and `brief-article-abt (Handoff Metadata suppressed…)` below are the two halves of what the flag does: here there was no other frontmatter and the file has none; there the artifact's own frontmatter is kept and only the map is gone.

## `brief-short` (genre that is not installed)

- **fixture** — `brief-short`
- **invocation** — `/write --genre=listicle <the brief's text, pasted inline>`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming `--genre=listicle` as no installed genre, listing the four that are installed, followed by the synopsis and a pointer to `/write --help`, and saying the brief is intact.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named in one line, the synopsis is printed, and the run stopped; the genre was refused rather than falling back to the default, which is the distinction that matters here.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — no corpus fixture stages an uninstalled genre; the fixture supplies the brief and the invocation supplies the fault.

## `brief-short` (read-only destination)

- **fixture** — `brief-short`, with `read-only-source` supplying the destination
- **invocation** — `/write --output=$RUN/corpus/output/readonly-source.md <the brief's text, pasted inline>`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming the destination as an existing file that is not writable, quoting its mode, followed by the synopsis and the help pointer, and stating that no file was created, none overwritten, no directory made, and no draft produced.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the condition was established by reading, before anything was drafted, and the refusal names it.
  - `effects` — `pass` — the inventory is identical before and after, the file is still mode `r--r--r--`, and `out/` is empty: no permission was changed and no result was written elsewhere as a substitute.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus stages this file for an In-place refusal, which Write has no gesture for; used as a destination it exercises the delivery contract's *a destination the run cannot write*, which is the nearest thing this Skill has to it.

## `brief-article-abt`

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=article --technique=abt --output=$RUN/out/shared-inbox.md Use the brief in $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/shared-inbox.md`
- **observed delivery** — the reply named the path and the resolved configuration, set out the arc in one paragraph, and named three things the angle would have used and the material does not carry; the draft was not repeated.
- **side effects** — `out/shared-inbox.md` created. Nothing else.
- **criteria** —
  - `fidelity` — `pass` — the dated events, the counted defect, the nine weeks, and the same team size are as the brief has them; the two stated limits are kept and are not resolved away.
  - `quotation` — `pass` — Miriam Adler is paraphrased rather than quoted, and the reply says why: the brief records what she said and not her words, so a fluent sentence in quotation marks would have claimed a record that does not exist. Nothing is attributed to her that she is not reported as saying.
  - `genre` — `pass` — `article` from the invocation, written for a reader of a trade publication who is not told what the tools are.
  - `technique` — `pass` — the ABT arc is there and is recognisable; the reply notes that the connectives are not written anywhere and the relations are, which is the technique rather than its vocabulary.
  - `language` — `pass` — `en_GB`, settled from the brief's day-month dates and *working days*.
  - `register` — `pass` — the trade-publication register the genre and audience call for, above the general baseline.
  - `handoff` — `pass` — a `kntnt` map with `article`, `abt`, `en_GB` and nothing else.
  - `stops` — `pass` — the reply says reviewing and proofreading are separate runs the user makes.
  - `target` — `pass` — exactly the named file was created.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — three gaps in the material, reported with the artifact.
- **defects filed** — none.
- **notes** — 725 words against the brief's roughly 700, which is the one run in this record that reached its stated length. The material carries enough here; the shorter drafts elsewhere are the material stopping, not the Skill.

## `brief-article-abt` (selectors normalized)

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=Article --technique=ABT --output=$RUN/out/inbox.md Use the brief in $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/inbox.md`
- **observed delivery** — the reply named the path, the resolved configuration in normalized spelling, and the arc; the draft was not repeated.
- **side effects** — `out/inbox.md` created. Nothing else.
- **criteria** —
  - `resolution` — `pass` — `Article` and `ABT` reached the installed resources, and the map on disk carries `article` and `abt` in the normalized spelling rather than the spelling that was typed.
  - `fidelity` — `pass` — the reply states, and the draft does, that the January accounts and the December count are adjacent in the record rather than cause and effect, which is precisely the join the brief does not make.
  - `technique` — `pass` — the arc is set out and is in the draft.
  - `handoff` — `pass` — normalized values in the map.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created.
- **unresolved findings** — five gaps in the material, reported with the artifact.
- **defects filed** — none.
- **notes** — none.

## `brief-article-abt` (Handoff Metadata merged with the artifact's own frontmatter)

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=article --technique=abt --output=$RUN/out/inbox.md Use the brief in $RUN/corpus/source/brief-article-abt.md -- It goes into our Jekyll site, so give it the frontmatter that needs: a title, layout: post, and a date of 2026-08-26.`
- **contextual instruction** — `It goes into our Jekyll site, so give it the frontmatter that needs: a title, layout: post, and a date of 2026-08-26.`
- **output target** — `$RUN/out/inbox.md`
- **observed delivery** — the reply named the path, said the Jekyll instruction had landed as a single frontmatter block rather than two, and named the title it had chosen.
- **side effects** — `out/inbox.md` created. Nothing else.
- **criteria** —
  - `handoff` — `pass` — the file on disk opens on one YAML block holding `title`, `layout: post`, `date: 2026-08-26`, and the `kntnt` map beneath them. One block, not two, which is what *merge it into the frontmatter the requested artifact already needs* asks for.
  - `fidelity` — `pass` — the reply names two fidelity decisions it made and both are the right ones: the eleven messages are not asserted to have each gone through the described routine, and Adler's *mostly* is preserved and pointed at.
  - `technique` — `pass` — the arc is stated and present.
  - `target` — `pass` — one file at the named path.
  - `effects` — `pass` — one file created.
- **unresolved findings** — four gaps in the material.
- **defects filed** — none.
- **notes** — the Contextual Instruction here narrows a choice the Skill leaves open rather than contradicting anything formal, which is what the Invocation Envelope permits it to do.

## `brief-article-abt` (Handoff Metadata suppressed, the artifact's own frontmatter kept)

- **fixture** — `brief-article-abt`
- **invocation** — `/write --genre=article --technique=abt --frontmatter=no --output=$RUN/out/inbox.md Use the brief in $RUN/corpus/source/brief-article-abt.md -- It goes into our Jekyll site, so give it the frontmatter that needs: a title, layout: post, and a date of 2026-08-26.`
- **contextual instruction** — `It goes into our Jekyll site, so give it the frontmatter that needs: a title, layout: post, and a date of 2026-08-26.`
- **output target** — `$RUN/out/inbox.md`
- **observed delivery** — the reply named the path and said explicitly that the flag and the instruction are not in conflict: the flag suppresses only the reserved map, and never the frontmatter the artifact itself needs.
- **side effects** — `out/inbox.md` created. Nothing else.
- **criteria** —
  - `handoff` — `pass` — the file on disk carries `title`, `layout: post`, `date: 2026-08-26` and no `kntnt` key at all. Turning the option off removed that map alone.
  - `fidelity` — `pass` — Adler paraphrased and said to be paraphrased; the causal join left unmade and said to be left unmade; the two stated limits kept in the closing paragraph.
  - `technique` — `pass` — the arc is present.
  - `target` — `pass` — one file at the named path, and the brief on disk is unchanged.
  - `effects` — `pass` — one file created.
- **unresolved findings** — five gaps in the material.
- **defects filed** — none.
- **notes** — this is the entry that shows the flag is narrow. A run that had read `--frontmatter=no` as *no frontmatter* would have dropped the Jekyll keys the same instruction asked for, and the reply would have had to choose between the flag and the instruction rather than honouring both.

## `brief-report-pac`

- **fixture** — `brief-report-pac`
- **invocation** — `/write --genre=report --technique=pac --output=$RUN/out/monitoring.md Use the brief in $RUN/corpus/source/brief-report-pac.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/monitoring.md`
- **observed delivery** — the reply named the path and the resolved configuration, said the material was spent at about 860 words against the requested 900, and named four gaps the draft leaves open rather than papering over.
- **side effects** — `out/monitoring.md` created. Nothing else.
- **criteria** —
  - `fidelity` — `pass` — the costs, the coverage counts, the twelve-month alert history, the four minutes, and the access-log date are as the brief has them. The two derived figures — €3,720 over a twelve-month term, and the second service at roughly 27 per cent of monitoring spend — are labelled in the text as arithmetic on the quoted prices rather than as terms anyone offered.
  - `technique` — `pass` — premise, analysis, conclusion, with the counter-argument inside the analysis rather than appended to it.
  - `genre` — `pass` — `report`, addressed to four people who approve a budget.
  - `language` — `pass` — `en_GB`, inferred from the brief's own *cancelling* and its date form.
  - `register` — `pass` — an internal budget report rather than an advocacy piece; the counter-argument is put at its strongest before it is answered.
  - `handoff` — `pass` — the map carries `report`, `pac`, `en_GB`.
  - `effects` — `pass` — one file created, nothing else touched.
- **unresolved findings** — four, and this is the entry where they matter most: the missing notice date, the absent base rate for the outage risk, the unknown identity of the eleven covered services, and the uncosted outage. The reply names the first as the one that could move the deadline rather than the argument.
- **defects filed** — none.
- **notes** — the fixture's rejection is *a draft that resolves the counter-argument by inventing evidence for or against it*. The draft answers the on-call lead on the overlap — eleven of forty-two — which is a fact the brief carries, and says explicitly that *we have never had a monitoring outage* cannot be turned into a probability without a base rate the material does not give. That is the counter-argument weighed rather than resolved.

## `brief-press-release-sv` (language inferred)

- **fixture** — `brief-press-release-sv`
- **invocation** — `/write --genre=press-release --output=$RUN/out/verkstad.md $RUN/corpus/source/brief-press-release-sv.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/verkstad.md`
- **observed delivery** — a Swedish reply naming the path and the resolved configuration, saying the material carries about 95 words of fact against a requested 350, and listing eight things that would close the gap.
- **side effects** — `out/verkstad.md` created. Nothing else.
- **criteria** —
  - `language` — `pass` — Swedish, inferred from the brief and the material with nothing above it in the precedence, and the whole report about the text is in Swedish too.
  - `fidelity` — `pass` — the date, the opening hours, the funding figure, and the two exclusions are as the brief has them; nothing suggests the workshop repairs devices for visitors or sells parts.
  - `quotation` — `pass` — Anna Lindqvist is reported in indirect speech, and the reply says why: the material reports what she says and does not give her words, so a direct quotation would have been invented.
  - `genre` — `pass` — `press-release` from the invocation.
  - `handoff` — `pass` — the map is attached.
  - `effects` — `pass` — one file created.
- **unresolved findings** — eight, including the missing year for 6 May.
- **defects filed** — none.
- **notes** — the reply states the principle the shortfall rests on: a requested length bounds how much of the material to use and is not permission to add. That is the behaviour issue #138 built, and this record is the first Claude-family record to see it on a fixture other than the two #138 was run against.

## `brief-press-release-sv` (language named explicitly against the material)

- **fixture** — `brief-press-release-sv`
- **invocation** — `/write --genre=press-release --language=en_GB --output=$RUN/out/workshop.md $RUN/corpus/source/brief-press-release-sv.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/workshop.md`
- **observed delivery** — an English reply naming the path and the resolved configuration, saying the Swedish brief settled nothing about the language because the invocation did, and listing what the material does not carry.
- **side effects** — `out/workshop.md` created. Nothing else.
- **criteria** —
  - `language` — `pass` — `en_GB` from the invocation, overriding a Swedish brief and Swedish material, which is the top of the precedence beating the bottom of it.
  - `fidelity` — `pass` — the exclusions survive translation; the reply flags that the material gives no year for 6 May and that the release therefore states none, and that `plan två` is rendered *level two* rather than a British floor number because the two systems do not line up.
  - `quotation` — `pass` — reported speech again, and the reply says an approved quotation would have to come from Anna Lindqvist.
  - `genre` — `pass` — `press-release`.
  - `handoff` — `pass` — the map is attached and names `en_GB`.
  - `effects` — `pass` — one file created.
- **unresolved findings** — seven, the missing year among them.
- **defects filed** — none.
- **notes** — about 130 words against a requested 350. The naming decisions — *Fagervik City Library*, the association's name left in Swedish — are reported as decisions rather than made silently, which is what the fixture's translation half is for.

## `interview-transcript`

- **fixture** — `interview-transcript`
- **invocation** — `/write --output=$RUN/out/halldin.md Write a short piece for a trade magazine for independent vehicle workshops about what changes when a workshop starts servicing electric vans. Audience: workshop owners. Length: about 450 words. Quote Petra Halldin where it helps. The interview is in $RUN/corpus/source/interview-transcript.md and is the only source.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/halldin.md`
- **observed delivery** — the reply named the path and the resolved configuration, listed five things the interview does not carry, and set out two fidelity decisions about the quotations.
- **side effects** — `out/halldin.md` created. Nothing else.
- **criteria** —
  - `quotation` — `pass` — this is the fixture's whole question, and the file on disk answers it. *So, I mean, the — okay, the first thing is, it's not the engine, everyone thinks it's the engine* is repaired to *"It's not the engine. Everyone thinks it's the engine,"* — fillers and the false start gone, the wording and the stance untouched. Her self-correction survives as an exclusion in her own words: eleven is full services, and *"There were more that came in for a tyre change or something — that doesn't count, I wouldn't count that."* Her hedges stand inside the quotation marks — *"We lost — I don't know — we lost weeks on that"*, and *"He said something like…"* keeps Jonas inside her attribution rather than promoting his words to a quotation of his own. Nothing in quotation marks is a sentence she did not say.
  - `fidelity` — `pass` — the eleven, the two mechanics, the three-day Gothenburg course, the twenty-two years, the one charger, and the warning about promising a date are as the transcript has them; the reply adds that whether she has approved these quotations is the user's arrangement and not something the run can establish.
  - `genre` — `pass` — `article` inferred for a trade magazine.
  - `language` — `pass` — `en_GB`, settled by the source's own *tyre* and its Gothenburg setting.
  - `register` — `pass` — a trade-magazine register for workshop owners.
  - `handoff` — `pass` — the map is attached.
  - `effects` — `pass` — one file created.
- **unresolved findings** — five, including the hedged *weeks* figure the reply declines to firm up.
- **defects filed** — none.
- **notes** — the fixture's rejection is a fluent invented quotation where fidelity is doubtful. Where fidelity was doubtful here — Jonas — the run paraphrased inside Halldin's attribution, which is the move the corpus names as correct.

## `factual-source-long`

- **fixture** — `factual-source-long`
- **invocation** — `/write --genre=report --output=$RUN/out/bus-route.md Write a summary for the transport committee of what the evaluation found. Audience: committee members who have not read it. Length: about 600 words. The evaluation is $RUN/corpus/source/factual-source-long.md and is the only source.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/bus-route.md`
- **observed delivery** — the reply named the path and the resolved configuration, described the draft's structure, and named five limits of the material.
- **side effects** — `out/bus-route.md` created. Nothing else.
- **criteria** —
  - `fidelity` — `pass` — every figure in the delivered file was checked against the source and every one of them is in it: 331,000 and 412,000, 268,000 and 312,000, 18,400, 63,000 against 62,600, 44 and 39 minutes, 10.6 and 8.2 million, the 3.1 million increase, the 2.4/0.7 split, 2.1 per cent, 4,000 households, 18 per cent, 71 and 6 per cent, 71 and 96 complaints, 29 and 12, 38, 34, 29, 21, and the dates 12 October 2023, 1 January 2024, 3 to 19 April, 14 January 2025. No number is in the draft that is not in the source.
  - `fidelity` (the four named rejections) — `pass` — no causal claim is made about any one of the three simultaneous changes, and the draft says so twice; the 71 per cent is reported as *of those* who replied, with the survey's own warning against reading it as a catchment figure carried over; the seventeen days are called *missing rather than zero*, in the operator's own terms; and the 2.4/0.7 split is labelled an estimate because the source labels it one.
  - `genre` — `pass` — `report`, structured top-line-first for a reader with a decision waiting.
  - `technique` — `pass` — none selected and none applied.
  - `language` — `pass` — `en_GB`, inferred and verified.
  - `register` — `pass` — the committee register the audience calls for.
  - `handoff` — `pass` — the map carries `report`, `none`, `en_GB`.
  - `effects` — `pass` — one file created.
- **unresolved findings** — five, the uncosted Kvarnvägen restoration and the unquantified ferry among them.
- **defects filed** — none.
- **notes** — the run also flagged that the source's own first line marks it as invented material, and kept that line out of the artifact because a summary addressed to the committee was what was asked for, offering to add it if wanted. That is a judgement about the artifact rather than about the facts, and it was reported rather than made silently.

## `url-source` (URL read, response default)

- **fixture** — `url-source`
- **invocation** — `/write Write a short explainer for developers who have just met the words MUST, SHOULD, and MAY in a specification and want to know what they commit to. Audience: working programmers, no standards background. Length: about 350 words. Use https://www.rfc-editor.org/rfc/rfc2119.txt and nothing else.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete draft in the response, frontmatter and all, followed by the resolved configuration and two things RFC 2119 does not settle.
- **side effects** — none.
- **criteria** —
  - `fidelity` — `pass` — the definitions are the RFC's, in its own terms: *absolute requirement*, *absolute prohibition*, the *valid reasons in particular circumstances* wording for SHOULD, and the interoperation obligation MAY carries in both directions. The draft attributes nothing to the RFC that the RFC does not give, and its two closing qualifications — that the force of the words is modified by the document's requirement level, and the security section's warning about subtle effects — are both the RFC's own.
  - `genre` — `pass` — `general` inferred, against the three named genres, none of which an explainer fits.
  - `technique` — `pass` — none selected, none applied.
  - `language` — `pass` — `en_US`, inferred from a US-authored IETF document with no variety marker in the request; *behavior* and *judgment* in the draft are consistent with it.
  - `handoff` — `pass` — the map carries `general`, `none`, `en_US`.
  - `target` — `pass` — no destination was named and the artifact stayed in the response; reading a URL selected nothing.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — two, both of them things the RFC does not say: how the uncapitalised words are to be read, and how a document's requirement level is determined.
- **defects filed** — none.
- **notes** — 361 words against a requested 350, so this is one of the two runs in the record whose material reached its stated length.

## `url-source` (filename derived from the URL)

- **fixture** — `url-source`
- **invocation** — `/write --output=$RUN/out <the same brief>`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the derived filename, said the destination was an existing directory and that nothing was overwritten, and listed three things the source does not carry.
- **side effects** — `out/key-words-for-use-in-rfcs-to-indicate-requirement-levels.md` created. Nothing else.
- **criteria** —
  - `target` — `pass` — no local file supplied the material, so the name came from the title of the referenced URL, which is the second of the three sources the delivery contract names, with a suitable text extension.
  - `fidelity` — `pass` — the same definitions, and the same three things named as outside the document rather than answered from elsewhere.
  - `genre` — `pass` — `general` inferred and named.
  - `language` — `pass` — `en_GB` here, inferred from the brief rather than the source, where the response-targeted run above read the source and landed on `en_US`.
  - `handoff` — `pass` — the map is attached.
  - `effects` — `pass` — one file created inside the named directory.
- **unresolved findings** — three.
- **defects filed** — none.
- **notes** — the two `url-source` runs resolved the language differently from the same material and the same brief — `en_US` from the source's own variety, `en_GB` from the brief's. Both readings sit at the fifth level of the precedence, where the parameter is inferred from *what was requested and what the material is*, and that phrase names both. Nothing distinguishes them, and neither draft carries a form wrong for the locale it named, so no criterion fails; the divergence is recorded because it is what an inferred locale looks like when the request and the material point different ways.

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/write --output=$RUN/out/second-server.md Write this up for our internal engineering newsletter. Audience: our own developers. Length: about 350 words. The account to work from is $RUN/corpus/prose/resembles-abt.md and it is the only source.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/second-server.md`
- **observed delivery** — the reply named the path and the resolved configuration, said in as many words that the account narrates itself with *But* and *Therefore* and reads as ABT but that a technique applies only when selected, and listed five gaps.
- **side effects** — `out/second-server.md` created. Nothing else.
- **criteria** —
  - `technique` — `pass` — this is the fixture's whole question. No technique was resolved, none was recorded in the map, and none was acted on, and the run names the temptation rather than yielding to it.
  - `handoff` — `pass` — the map carries `technique: none`, not `abt`.
  - `fidelity` — `pass` — the run lists the thirteen facts it traced and asserts nothing else: 2016, nine requests a minute, one disk replacement, the sole login, March, four hundred, the seek-bound slowdown, 90 ms to just over two seconds, eleven unmonitored days, the second machine on the same address, 140 ms within an hour, four days of arguing, and the argument written down.
  - `genre` — `pass` — `general` inferred for an internal newsletter.
  - `language` — `pass` — `en_GB`.
  - `effects` — `pass` — one file created.
- **unresolved findings** — five.
- **defects filed** — none.
- **notes** — the fixture's rejection is *a resolved technique of ABT reported, recorded in metadata, or acted on when nothing selected it*. None of the three happened, and the metadata on disk is the evidence for the second.

## `mixed-language` (nothing named)

- **fixture** — `mixed-language`
- **invocation** — `/write Turn these retrospective notes into a short summary for the team. Length: about 250 words. The notes are $RUN/corpus/prose/mixed-language.md and they are the only source.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — one question and nothing else: the reply quoted a code-switching sentence, said the Swedish carries the load-bearing sentences and the English the blocker and the closing line, named the three installed candidates, and asked which to write in. It set out everything else it had already resolved, and flagged separately that the notes are thin against 250 words.
- **side effects** — none.
- **criteria** —
  - `ask` — `pass` — the language was asked about rather than guessed, before anything was written, which is what the Skill's step 3 requires of materially mixed material.
  - `resolution` — `pass` — the four parameters the material could settle were settled, and only the one it could not was put to the user. An invocation is not held up wholesale by one open parameter.
  - `effects` — `pass` — the inventory is identical before and after, so the question cost nothing to leave unanswered.
- **unresolved findings** — the language, and the thinness of the material against the requested length.
- **defects filed** — none.
- **notes** — the reply's reasoning for asking is the fixture's own: the brief is in English, but the brief being in English says little when the team whose retrospective it is demonstrably writes in both.

## `mixed-language` (language named)

- **fixture** — `mixed-language`
- **invocation** — `/write --language=sv --output=$RUN/out/retro.md <the same brief>`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/retro.md`
- **observed delivery** — a Swedish reply naming the path and the configuration, saying that with `--language=sv` on the invocation there was nothing to ask about, and listing five things the notes do not carry.
- **side effects** — `out/retro.md` created. Nothing else.
- **criteria** —
  - `language` — `pass` — `sv` from the invocation, and the draft is Swedish throughout with no English passage carried over untranslated.
  - `ask` — `pass` — no question was asked where the invocation had already settled the parameter, which is the other half of what the fixture stages.
  - `fidelity` — `pass` — every claim traces to a line in the notes; the reply names *what the DBA actually said* as absent and does not supply it.
  - `genre` — `pass` — `general` inferred for an internal note.
  - `handoff` — `pass` — the map is attached.
  - `effects` — `pass` — one file created.
- **unresolved findings** — five, including what *heller* refers back to, which the reply notes the material does not say.
- **defects filed** — none.
- **notes** — 108 words against a requested 250, from notes that are themselves under 130 words.

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/write --output=$RUN/out/archive.md Write this up as a piece the board can read before its meeting. Length: about 450 words. Work from $RUN/corpus/frontmatter/handoff-present.md and nothing else.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/archive.md`
- **observed delivery** — the reply named the path and said all three parameters came from the `kntnt` map in the source's frontmatter, which sits above inference; it added that had the genre been open, *a piece the board can read* would have pointed at `report` rather than `article`, and offered to re-run.
- **side effects** — `out/archive.md` created. Nothing else.
- **criteria** —
  - `resolution` — `pass` — genre, technique, and language all fell through to the map, which is the second level of the precedence and the level this fixture stages; the map's values were reported in the normalized spellings it carries.
  - `technique` — `pass` — `abt` because the map selected it, and the draft carries the arc.
  - `genre` — `pass` — `article`, and the run names explicitly that the map beat an inference that would have gone the other way. That is precedence working rather than an accident.
  - `language` — `pass` — `en_GB` from the map, matching the English body.
  - `fidelity` — `pass` — the nine facts the source carries, all used, none added; the draft ends on the source's own open question rather than manufacturing a recommendation, and the reply says so.
  - `handoff` — `pass` — the delivered map carries `article`, `abt`, `en_GB`.
  - `stops` — `pass` — reviewing and proofreading named as separate runs not performed.
  - `effects` — `pass` — one file created.
- **unresolved findings** — six gaps, and the absence of an ask in the source.
- **defects filed** — none.
- **notes** — none.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/write --genre=article --language=sv --output=$RUN/out/felanmalan.md Skriv om det här till en artikel för vår kundtidning. Längd: ungefär 450 ord. Källan är $RUN/corpus/frontmatter/handoff-conflicting.md och inget annat.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/felanmalan.md`
- **observed delivery** — a Swedish reply naming the path and setting out the split explicitly: genre and language from the invocation, technique from the map, and the map's `genre: report` and `language: en_US` suppressed by the invocation above them.
- **side effects** — `out/felanmalan.md` created. Nothing else.
- **criteria** —
  - `resolution` — `pass` — this is the fixture's whole question and the run answers it per field. No metadata value overrode an explicit one, and an explicit value for two parameters did not suppress the map for the third.
  - `technique` — `pass` — `pac` taken from the map, which is where the fixture leaves it, and the draft is premise-analysis-conclusion.
  - `genre` — `pass` — `article` from the invocation.
  - `language` — `pass` — `sv` from the invocation, over a map that says `en_US` and a body that is Swedish anyway.
  - `handoff` — `pass` — the delivered artifact carries a `kntnt` map of `article`, `pac`, `sv` — the configuration the run actually resolved, not the one the source's map claimed. That is the corpus's third rejection, and it did not happen.
  - `fidelity` — `pass` — the source's two explicit uncertainties survive as uncertainties, and the before-and-after on median first response is written as a before and an after rather than as an established cause.
  - `effects` — `pass` — one file created.
- **unresolved findings** — five.
- **defects filed** — none.
- **notes** — the run reports removing two sharpenings on a self-check: a twenty-minute *interval* where the source says a twenty-minute *watch*, and a claim about thin summer staffing the source never makes. Both are Source Fidelity failures caught before delivery rather than after.

## `handoff-partial`

- **fixture** — `handoff-partial`
- **invocation** — `/write --genre=report --output=$RUN/out/nyhetsbrev.md Write this up for the people who have to take the decision. Length: about 400 words. The note to work from is $RUN/corpus/frontmatter/handoff-partial.md and it is the only source. -- Write it in Swedish.`
- **contextual instruction** — `Write it in Swedish.`
- **output target** — `$RUN/out/nyhetsbrev.md`
- **observed delivery** — a Swedish reply naming the path and the three levels that settled the three parameters, and listing four things the note does not carry.
- **side effects** — `out/nyhetsbrev.md` created. Nothing else.
- **criteria** —
  - `resolution` — `pass` — the fixture's whole point, and all three levels answered in one run: the invocation settled the genre, the map settled the technique, and the Contextual Instruction settled the language the map leaves absent and the text cannot supply.
  - `technique` — `pass` — `abt` from the map, neither refused for the map's incompleteness nor taken from anywhere else.
  - `ask` — `pass` — no language question was asked, because the Contextual Instruction had already named one; the material would otherwise have forced one, being the same alternating Swedish and English `mixed-language` uses.
  - `language` — `pass` — Swedish throughout, from the instruction.
  - `fidelity` — `pass` — the reply names the asymmetry the note carries and the draft keeps it: the first option has a time and a cost, the second has neither, so the two cannot be compared on money and the draft says so instead of filling the gap. It makes no recommendation, because the note says nobody knows which option matters more.
  - `handoff` — `pass` — the map carries the resolved values.
  - `effects` — `pass` — one file created.
- **unresolved findings** — four.
- **defects filed** — none.
- **notes** — the two absent keys were not read as a reason to stop, to ask for a complete map, or to treat the map as unusable, which is the fixture's first rejection.

## `handoff-unusable`

- **fixture** — `handoff-unusable`
- **invocation** — `/write --output=$RUN/out/stop.md Write this up for the committee's next agenda. Length: about 300 words. Work from $RUN/corpus/frontmatter/handoff-unusable.md and nothing else.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/stop.md`
- **observed delivery** — a report of unusable artifact metadata: the reply quoted the map, quoted the resolver's own message that `en_UK` reaches no installed Language Resource and named the three that are installed, said that a language in a map is never quietly read as the nearest usable value, and set out both ways to proceed.
- **side effects** — none.
- **criteria** —
  - `resolution` — `pass` — `en_UK` was not read as `en_GB`; the map outranks inference and the invocation settled only `--output`, so nothing below it could settle the language either, and the run stopped.
  - `refusal` — `pass` — the problem is named, and the run reports what it had already resolved — `article` and `abt` from the same map, both usable — rather than discarding the whole map over one value.
  - `effects` — `pass` — the inventory is identical before and after; `out/stop.md` does not exist and the source is untouched.
- **unresolved findings** — none; the run stopped rather than delivering.
- **defects filed** — none.
- **notes** — the run also flagged, without acting on it, that the material is two short paragraphs and would not have supported 300 words. That is a useful thing to have said, and it is said as an observation rather than as a second reason to stop.

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/write --output=$RUN/out/estimating.md Rework this into a short piece for our team handbook. Length: about 300 words. The source is $RUN/corpus/frontmatter/frontmatter-unrelated.md and nothing else.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/estimating.md`
- **observed delivery** — the reply named the path and stated that `genre: fiction`, `technique: montage`, `language: Esperanto` and `lang: fr` sit at the top level rather than under a reserved `kntnt` key, so the block is ordinary document metadata and configured nothing.
- **side effects** — `out/estimating.md` created. Nothing else.
- **criteria** —
  - `resolution` — `pass` — none of the four bait keys was read as configuration; genre fell to `general` by inference and language to English from the request and the body.
  - `handoff` — `pass` — the delivered file carries the `kntnt` map alone. The source's own Jekyll keys were not carried across, and the reply says why: they belong to its blog rather than to a handbook piece.
  - `fidelity` — `pass` — nothing in the draft is absent from the source; the reply notes that the source is titled *Three notes on estimating* and carries only two, and titles the draft *Two notes* rather than promising one it cannot deliver.
  - `language` — `pass` — English, with the `fr` and `Esperanto` keys treated as data in the file rather than evidence about the text.
  - `effects` — `pass` — one file created.
- **unresolved findings** — two, the missing third note among them.
- **defects filed** — none.
- **notes** — the missing third note is a good example of the difference between reporting a gap and filling one: a run that had written a third note would have satisfied the title and broken the invariant.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/write --output=$RUN/out/duty-roster.md Rework this into a short piece for our team handbook. Length: about 300 words. The source is $RUN/corpus/frontmatter/frontmatter-absent.md and nothing else.`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/duty-roster.md`
- **observed delivery** — the reply named the path and the resolved configuration, said the source carries no frontmatter so nothing in it configured the run, and reported roughly 170 words against a source of about 165.
- **side effects** — `out/duty-roster.md` created. Nothing else.
- **criteria** —
  - `resolution` — `pass` — no metadata was demanded and nothing was refused; every parameter fell through to inference or its default.
  - `fidelity` — `pass` — three claims and their consequence, and no case, figure, or named team invented to reach the length.
  - `genre` — `pass` — `general` inferred.
  - `language` — `pass` — `en_GB`, settled by the source's own *artefact* and *rota*.
  - `handoff` — `pass` — the map is attached to an artifact that had no frontmatter of its own.
  - `effects` — `pass` — one file created.
- **unresolved findings** — three.
- **defects filed** — none.
- **notes** — this is the baseline the fixture exists for, and the Skill remains usable with no metadata at all.

## `response-default`

- **fixture** — `response-default`
- **invocation** — `/write Rework this into a short piece for our team handbook. Length: about 300 words. The source is $RUN/corpus/frontmatter/frontmatter-absent.md and nothing else.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete draft in the response, frontmatter and all, followed by the resolved configuration, one editorial decision flagged, and what would close the length gap.
- **side effects** — none.
- **criteria** —
  - `target` — `pass` — the reply states the rule and the filesystem confirms it: naming a source file selects no destination, so nothing was written.
  - `effects` — `pass` — no file was created, replaced, or removed anywhere under the working copy.
  - `fidelity` — `pass` — 165 words against a source of 169, with nothing added.
  - `handoff` — `pass` — the map is in the delivered text.
  - `stops` — `pass` — the reply closes by saying this was a drafting pass only and that no review or proofreading was run.
- **unresolved findings** — four things that would close the gap to 300 words.
- **defects filed** — none.
- **notes** — the run flagged one editorial decision rather than making it silently: the source names the same thing *duty roster* and *rota*, and the draft keeps one of the two so that a handbook reader does not have to work out that they are the same thing. That is a wording choice inside a rewrite rather than a new fact, and reporting it is the right side of the line.

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/write --output=$RUN/corpus/output/collision Write these interview notes up as a short piece for a trade magazine. Length: about 300 words. The notes are $RUN/corpus/output/interview-notes.md and they are the only source.`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the reply named the file written, said the derived name came from the source's own basename, that `interview-notes.md` and `interview-notes-2.md` were occupied, and that the draft took the first free candidate.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants and the source are byte-unchanged.
- **criteria** —
  - `target` — `pass` — the stem stayed `interview-notes` and the first free candidate in ascending order was taken; `interview-notes-2-2.md`, the name the corpus names as the wrong answer, was not written.
  - `fidelity` — `pass` — the run declines to write *electric*, because the notes say *vans*, *high-voltage course*, and *charger* and never state the drivetrain. That is a smaller inference than most runs would trouble to refuse, and refusing it is the invariant working.
  - `quotation` — `pass` — the notes are paraphrase with no verbatim speech, so everything attributed to Halldin is attributed as report and nothing is put inside quotation marks.
  - `genre` — `pass` — `article` inferred for a trade magazine.
  - `handoff` — `pass` — the map is attached.
  - `effects` — `pass` — one file created, neither occupant overwritten.
- **unresolved findings** — four.
- **defects filed** — none.
- **notes** — none.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/write --output=$RUN/corpus/output/in-place-source.md Rework this into a short piece for our team handbook. Length: about 300 words. The source is $RUN/corpus/output/in-place-source.md and nothing else.`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming the output path as the same local file the brief supplies as material, followed by the synopsis and the help pointer, and saying that `write` creates a text and never replaces the material its brief came from.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named, the synopsis printed, and two alternatives offered; the refusal points at the reason rather than at a gesture, since this Skill has no In-place Editing to point at.
  - `effects` — `pass` — the file was not replaced and the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `<no brief>`

- **fixture** — none; the Skill's own `## Arguments` list names *nothing to write* as a refusal and the corpus stages no fixture for it.
- **invocation** — `/write`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — one line — *Nothing to write: the invocation carries no brief, no material, and no applicable guidance in context* — followed by the synopsis and the help pointer.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the problem is named, the synopsis printed, and nothing was invented to write about.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `<uninstalled technique>`

- **fixture** — `brief-article-abt` supplies the brief; the invocation supplies the fault.
- **invocation** — `/write --genre=article --technique=montage --output=$RUN/out/inbox.md Use the brief in $RUN/corpus/source/brief-article-abt.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming `--technique=montage` as not installed and listing `abt` and `pac`, followed by the synopsis, the help pointer, and a statement that no file was created at the named path.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the technique was verified against what is installed and refused rather than dropped, which is the counterpart to the uninstalled-genre refusal above.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — `montage` is also one of `frontmatter-unrelated`'s bait keys, which is why it is the value used here.

## `<the brief written before an option>`

- **fixture** — `brief-article-abt` supplies the brief; the invocation supplies the fault.
- **invocation** — `/write Use the brief in $RUN/corpus/source/brief-article-abt.md --genre=article --technique=abt`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming the out-of-order form, followed by the synopsis, the help pointer, and the same invocation written in order.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the run establishes that both named resources are installed and refuses anyway, on the order alone; the fault is named as the order and not as anything else.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the invocation is unambiguous to a reader and was still refused rather than repaired, which is what the Skill's `## Arguments` list describes.

## `<undeclared flag>`

- **fixture** — `in-place-request` supplies the file; the invocation supplies the fault.
- **invocation** — `/write --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — refused
- **observed delivery** — a refusal naming `--in-place` as a `--`-prefixed token outside the five accepted options, followed by the synopsis and the help pointer, and a paragraph saying that `write` has no in-place mode by design.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the flag was refused rather than ignored, nothing was read from the file, and the reply explains the design reason rather than only the grammar.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus stages `in-place-request` and `output-and-in-place` for Skills that have In-place Editing. Write does not, so both reach it as an undeclared flag; this entry is the half of them that is reachable, and the pair is recorded among the skipped fixtures below.

## Fixtures deliberately skipped

Nine fixtures were not run against this Skill. Each is recorded here rather than omitted, because a record silently missing a fixture reads later as a fixture that passed.

- `clean-en-GB` — `skipped` — mechanically clean prose whose rejections are about a mechanical pass finding nothing and a review declining to rewrite competent writing. Write creates a text rather than returning a changed version of one; used as material it would exercise nothing `frontmatter-absent` and `resembles-abt` do not already establish about drafting from a finished piece of prose.
- `flawed-en-US` — `skipped` — its rejections are entirely about what a mechanical pass may and may not correct. Write performs no proofreading pass at all, which is what `stops` records on every entry above.
- `flawed-sv` — `skipped` — same reason. Swedish composition is exercised by `brief-press-release-sv`, `handoff-conflicting`, `handoff-partial`, and `mixed-language (language named)`.
- `slop-heavy` — `skipped` — an anti-slop fixture. Its rejections judge a review that names patterns; Write runs no review, and a draft written from it would be judged on Source Fidelity, which four other fixtures already stage against far more demanding material.
- `slop-heavy-sv` — `skipped` — same reason.
- `code-carrying` — `skipped` — its rejections are about a pass that changes a text around code samples and must leave the samples byte for byte. Write does not edit a supplied text, so there is no diff against the fixture to judge; the corpus's own entry says a run that changes nothing shows nothing there, and a run that writes something new is not the pass it is describing.
- `code-carrying-sv` — `skipped` — same reason.
- `locale-divergent` — `skipped` — its rejections are locale mechanics applied to an existing note under each English locale in turn. Write's language parameter is exercised at every level of the precedence by the fixtures above, and Write applies no mechanics scope: the resolver is called with `--scope=composition`.
- `in-place-request` and `output-and-in-place` — `skipped` as In-place fixtures. Write has no In-place Editing, by design, so neither can be staged as the corpus intends. What is reachable of them is recorded above: the file appears as an `--output` destination equal to a supplied source in `output-equals-source`, and `--in-place` appears as an undeclared flag in `<undeclared flag>`.

## What this record establishes, and what it does not

Thirty-four fixture runs. Thirty-three are clean; one carries two failing criteria. On `brief-short` supplied inline with no destination named, the draft came back in the response and a complete copy of it was also left on disk in the Harness's scratchpad, with the run reporting that nothing had been written. That is filed as #180, and it was found during cleanup rather than during judging — the inventories covered the staged corpus copy and not the ground outside it, which is now said under **Run conditions**.

Source Fidelity is the invariant these runs were most likely to break and did not. Every figure in the `factual-source-long` draft was checked against the source and every one of them is in it; all four of that fixture's named rejections were avoided, and the two the draft could most easily have committed — a causal claim about one of three simultaneous changes, and a survey figure quoted as a catchment figure — are declined in the draft's own words. `interview-transcript` came back with the fillers gone, the hedges standing, the self-correction preserved as the exclusion it is, and the one doubtful attribution paraphrased inside the speaker's own. Two runs report deleting sentences of their own on a final check, one of them a *twenty-minute interval* where the source says a twenty-minute *watch*.

The resolution order held at every level the corpus can stage, including all three at once: `handoff-partial` settled its genre from the invocation, its technique from the map, and its language from the Contextual Instruction in one run. `resembles-abt` recorded `technique: none` in metadata for a text that opens its third paragraph with *Therefore*. `frontmatter-unrelated`'s four bait keys configured nothing. `handoff-conflicting` delivered a map describing what the run resolved rather than what the source claimed.

Twenty-five of the thirty-four runs delivered a draft. Five reached their stated length, within the margin the briefs allow; the other twenty came back short of it, every one of them naming the shortfall and listing the material that would close it. Several are far short — 130 words against 350, 108 against 250, 165 against 300 — and each says the same thing in its own words: a requested length bounds how much of the material to use rather than licensing addition. That is the behaviour issue #138 built, and this is the first Claude-family record to see it across the whole corpus rather than on the two fixtures #138 was re-run against.

Nothing in this record establishes anything about the Skill under a Harness other than Claude Code, and nothing about it under the ordinary slash-command path: every run here was given the Skill's instructions the way the **Run conditions** describe, because the Skill's own `disable-model-invocation` flag makes the other path unreachable from a sub-session. What that flag protects is intact and was observed sixteen times over: the Skill will not start itself.

## Runs discarded

**Sixteen model-invocation attempts.** Before the method under **Run conditions** was settled, sixteen runs were driven by handing a sub-session the invocation alone. Every one of them tried to start the Skill through the Skill tool, was refused because `disable-model-invocation: true`, declined to reproduce the Skill's work by hand, declined to substitute the legacy `kntnt-text-skills:write` plugin, wrote nothing, and asked the user to run `/write` themselves. They are named here so the count of turns spent is honest. They carry no criteria — they say something about the Harness seam and nothing about what the Skill does with a brief — and every fixture they touched was re-run from a fresh working copy.

**One `brief-short` run, response default.** An earlier run of the inline-material invocation wrote `draft.md` at the root of its working copy although the invocation named no destination. That run's harness framing carried a sentence saying which directory any file it wrote belonged under — a sentence meant to keep a stray write inside the working copy, which a run could reasonably read as a destination. It is therefore discarded rather than recorded as a `target` failure: the ambiguity is the harness's and not the Skill's. The invocation was re-run from a fresh working copy with that sentence removed, and the re-run wrote nothing at all, which is the entry this record holds. Two other runs carried the same sentence — the uninstalled-genre refusal and `mixed-language (nothing named)` — and neither wrote anything, one having refused and the other having asked.
