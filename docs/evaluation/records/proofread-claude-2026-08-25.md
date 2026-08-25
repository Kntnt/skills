# proofread — claude — 2026-08-25

- **record** — `proofread-claude-2026-08-25`
- **date** — `2026-08-25`
- **ticket** — `#107`
- **skill** — `proofread`
- **provider family** — `claude`
- **model** — `claude-opus-5`
- **harness** — Claude Code 2.1.245
- **corpus commit** — `e2e162c`

## Run conditions

The Skill was run as a user of it runs it: `/proofread …` typed into a Claude Code turn, against the Skill as installed at `~/.agents/skills/proofread`, which was byte-identical to `skills/editorial/proofread/` at the corpus commit (`diff -r` reported no difference, as it did for `skills/kntnt/` and its Collection Library). Nothing in this repository was read by the runs, and no run was given the Skill's own instructions, the ticket, or the criteria below.

Each fixture ran in its own turn with no memory of any other, and in its own copy of the corpus, staged exactly as [`../corpus/README.md`](../corpus/README.md) says: `cp -R docs/evaluation/corpus`, an empty `out/` beside it, and `chmod a-w` on `output/readonly-source.md`. `$RUN` below abbreviates that copy's root, `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/107.scratch/runs/<id>`; invocations are otherwise verbatim, and the paths as typed carried the unabbreviated form. **side effects** is read from a `sha256` inventory of the whole working copy taken before and after each run, never from what the run said about itself.

Two conditions of this machine are worth a later reader's attention, because both shaped how the runs were driven.

- **`/proofread` is ambiguous here.** A legacy plugin, `kntnt-text-skills:proofread`, is installed beside the Collection's Skill and answers to the same bare name. Ten runs driven with no disambiguation went to the plugin instead of the Skill under evaluation, and are discarded rather than recorded: they are a fact about this machine's installed plugins, not about this Skill. Every by-name run below therefore carried one added routing sentence — that two Skills answer to `proofread` here, that the user means the Skill named exactly `proofread`, and that the plugin is not it. The sentence names which Skill to start and says nothing about what to do once it starts. The legacy project is prior art the specification puts out of scope, so the collision is recorded here and filed against nothing.
- **Model invocation was tested without that sentence**, since a routing hint would decide the very thing those runs exist to observe. Their entries name which Skill actually started.

Judging was done from the delivered reply and the filesystem inventory alone, against the criteria below, fixture by fixture, before any GPT-family record existed to compare with. No Codex Harness and no GPT model was started, controlled, or invoked from this session, directly or through any tool, script, or subagent.

The criterion identifiers are stable across entries: `trigger` (the Skill started, or did not, as the description bounds it), `language` (the resolved language is the one the precedence names), `mechanics` (the mechanical layer is corrected), `preserve` (everything else comes through untouched, valid alternatives included), `no-drift` (no stylistic improvement), `status` (the short no-change status where the contract asks for one), `target` (the artifact went where the output contract sends it), `effects` (the filesystem shows what the contract allows and nothing else), `refusal` (a refused invocation names the problem, prints the synopsis, and leaves nothing behind).

## `flawed-en-US`

- **fixture** — `flawed-en-US`
- **invocation** — `/proofread $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete corrected text came back in the response, in a fenced block, followed by a list of the fourteen corrections and a note of what was left as valid choice; nothing was written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — resolved `en_US` by inference from the text's own `normalize` and `catalog`, with no flag, no frontmatter, and no instruction in play.
  - `mechanics` — `pass` — `writen`, `writting`, `It's job`, `Its that`, `into into`, `wasnt`, `dont`, `isnt`, `doesnt`, `would of been`, `The bug were`, `differences was`, `for four year`, and the US placement of the full stop inside `"rewrite things."` were all corrected.
  - `preserve` — `pass` — the American spellings, the heading, the paragraphing, the spaced em dashes, the hedges, and the closing opinion are unchanged; the diff against the fixture touches nothing but the errors.
  - `no-drift` — `pass` — no sentence was restructured and nothing was tightened, in a text whose third paragraph invites both.
  - `target` — `pass` — no destination was named and the response received the artifact.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — #125.
- **notes** — the comma in *The bug were not in the parsing at all, it was in a silent retry* was left, and named in the reply as a preference rather than an error. Every other run over this fixture did the same, for the same stated reason. That was filed as the defect #125, on the corpus's premise that the sentence carried a planted comma splice. It did not: checked against Garner, the Chicago Manual's Q&A, and Språkrådet, the negative-positive joint is accepted usage in both shipped languages, and the retention and the reason given for it were both correct. #125 was rewritten to say so, and what it built is the written rule the runs had none of — the entry stands as it was judged, and the defect it names was the corpus's, not the Skill's.

## `flawed-en-US` (In-place Editing)

- **fixture** — `flawed-en-US`
- **invocation** — `/proofread --in-place $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place
- **observed delivery** — the reply reported the file replaced and listed the corrections; the corrected text was not repeated in full.
- **side effects** — `corpus/prose/flawed-en-US.md` replaced. Nothing else created, replaced, or removed.
- **criteria** —
  - `mechanics` — `pass` — the file on disk carries the same fourteen corrections.
  - `preserve` — `pass` — the replaced file is byte-identical to the corrected text the response-targeted run returned for the same fixture, so neither destination changed what correction means.
  - `target` — `pass` — the source file itself received the result, and no copy was left beside it.
  - `effects` — `pass` — exactly one file changed, and it is the one named.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — that same comma is untouched here too, correctly; see the note on the entry above and #125.

## `flawed-sv`

- **fixture** — `flawed-sv`
- **invocation** — `/proofread $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reply was written in Swedish, listed six corrections, and returned the complete corrected text; nothing was written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — Swedish was inferred from the text and the whole exchange was conducted in it, with no English answer anywhere in the reply.
  - `mechanics` — `pass` — every planted error was corrected: `det det`, `dem svåra` → `de svåra`, `uptäckte` → `upptäckte`, the split compound `avgångs samtal` → `avgångssamtal`, and the missing word in `vi tänker inte gå tillbaka`; the inflection `Antalet ärende` → `ärenden` was corrected with them.
  - `preserve` — `pass` — `hen` stands, which the fixture names as the trap: it is a valid Swedish pronoun and not an error.
  - `no-drift` — `pass` — the argument, the paragraph order, and the numbers are as they were.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the fixture that shows mechanical correction is language-specific in practice and not only in the contract; it is.

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
- **notes** — the discarded plugin run over this same fixture changed an em dash to an en dash, which is one reason those runs are discarded rather than recorded: the difference between the two Skills is visible on exactly the fixture built to catch it.

## `clean-en-GB` (unchanged result, explicit different file)

- **fixture** — `clean-en-GB`
- **invocation** — `/proofread --output=$RUN/out/clean-copy.md $RUN/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/clean-copy.md`
- **observed delivery** — the reply said no mechanical errors were found, and that the complete text had been written to the named path anyway because an explicit different destination was chosen.
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
- **observed delivery** — a short status: no mechanical errors found, nothing written, and one sentence saying that style, wording, and structure were left alone by design.
- **side effects** — none.
- **criteria** —
  - `no-drift` — `pass` — the empty opening, the *it's not X — it's Y* contrasts, the vague attributions, and the closing rhetorical question all survive a pass that was asked only for mechanics.
  - `preserve` — `pass` — nothing in the text changed.
  - `status` — `pass` — the short status came back rather than a repeated text.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the corpus's strongest temptation to improve a text, and the run named the temptation and declined it. Finding the slop is Redline's job and not this one's; nothing here judges whether the patterns are findable.

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/proofread $RUN/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a one-line no-change status; nothing written.
- **side effects** — none.
- **criteria** —
  - `no-drift` — `pass` — a competent text came back untouched, including the paragraph that opens on *Therefore*.
  - `status` — `pass` — the short status, not the text.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — technique is not a Proofread parameter, so the fixture's own trap cannot be sprung here; what it tests for this Skill is that a text shaped like something is not treated as an invitation to shape it further. No technique was reported, recorded, or acted on.

## `mixed-language`

- **fixture** — `mixed-language`
- **invocation** — `/proofread $RUN/corpus/prose/mixed-language.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no correction: the reply quoted two of the alternating passages, said the language could not be settled, and asked which language to proofread in, offering `sv`, `en_GB`, and `en_US` as the formal values.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — material with no dominant language produced a question rather than a silently chosen locale, which is what the fixture exists to catch.
  - `effects` — `pass` — nothing was written, so the question costs nothing to answer either way.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the reply also observed that the path looked like corpus material. That is a remark about the file's location, not a reading of its content, and it changed nothing about the run.

## `locale-divergent` (en_GB)

- **fixture** — `locale-divergent`
- **invocation** — `/proofread --language=en_GB $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status, with the British forms it had checked and accepted named one by one; nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the flag resolved `en_GB` and the mechanics applied were that locale's.
  - `preserve` — `pass` — `organised`, `specialised`, `cancelling`, `licence` as a noun against `licensed` as a verb, `judgement`, `£14,500`, and `3/4` all stand, none of them treated as an error.
  - `mechanics` — `pass` — the closing full stop outside the quotation was correct for this locale and was left there.
  - `status` — `pass` — the short status rather than a repeated text.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the ambiguous `3/4` was left as written, which is the fixture's own rejection: an unambiguous date here would be an asserted fact.

## `locale-divergent` (en_US)

- **fixture** — `locale-divergent`
- **invocation** — `/proofread --language=en_US $RUN/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the complete corrected text in the response, with the corrections and the deliberate omissions both listed; nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the flag resolved `en_US`, and the same file that was clean under `en_GB` produced seven corrections under this locale, so the resolved locale demonstrably reaches the mechanics.
  - `mechanics` — `pass` — `organised`, `specialised`, `judgement`, `cancelling`, and the noun `licence` were converted to the American forms, the full stop moved inside the closing quotation mark, and `has got harder` became `has gotten harder`.
  - `preserve` — `pass` — `£14,500` was left as a fact about the currency rather than rewritten, `3/4` was left ambiguous rather than resolved on an assumption, and `autumn` was left as a word choice.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this run was driven without the routing sentence and reached the Skill under evaluation anyway; the reply names the resolved code and the mechanics scope, which the plugin's replies never do.

## `locale-divergent` (contextual instruction)

- **fixture** — `locale-divergent`
- **invocation** — `/proofread $RUN/corpus/prose/locale-divergent.md -- This note is for our American readers, so apply American English mechanics.`
- **contextual instruction** — `This note is for our American readers, so apply American English mechanics.`
- **output target** — `response`
- **observed delivery** — the complete corrected text under American mechanics, with the corrections listed and the two deliberate omissions explained; nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — with no flag and no `kntnt` map, the Contextual Instruction settled the locale as `en_US`, ahead of an inference that the file's own British forms would otherwise have made, which is the precedence step this run exists for.
  - `mechanics` — `pass` — the same American corrections as the flagged run.
  - `preserve` — `pass` — `£14,500` and `3/4` again untouched, and the reply says why rather than acting.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/proofread $RUN/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status naming British English as the mechanics applied; nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — with nothing formal supplied, the `kntnt` map's `language: en_GB` decided the locale, and the reply names it in that normalized spelling.
  - `preserve` — `pass` — the frontmatter is byte-identical, and no `kntnt` value was rewritten, reordered, or reported in another spelling.
  - `status` — `pass` — the short status rather than a repeated text.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — genre and technique sit in the same map and were not read; this Skill is entitled to the language value and nothing else, and the reply mentions neither.

## `handoff-present` (metadata against a contrary instruction)

- **fixture** — `handoff-present`
- **invocation** — `/proofread $RUN/corpus/frontmatter/handoff-present.md -- Apply American English mechanics to this one.`
- **contextual instruction** — `Apply American English mechanics to this one.`
- **output target** — `response`
- **observed delivery** — no correction: the reply named the guidance, quoted the `kntnt` map that had already answered the language, said that guidance may narrow a choice the Skill leaves open but not override one the document has made, reported that nothing had been written, and pointed at `--language=en_US` as the formal way to get what was asked.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — recognized Handoff Metadata outranked the Contextual Instruction, and no American mechanics were applied.
  - `refusal` — `pass` — the contradictory guidance took the documented context refusal: the guidance and the boundary are named, the mutation outcome is stated, and no synopsis is printed, which is the form that refusal is specified in.
  - `effects` — `pass` — nothing was written, and no half of the request was carried out.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run stops rather than proceeding silently under `en_GB`. Both readings leave the metadata in charge, which is what the precedence requires; stopping additionally tells the user that what they asked for did not happen, which a silent continuation would not.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/proofread --language=sv $RUN/corpus/frontmatter/handoff-conflicting.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status in Swedish, saying that `--language=sv` had taken precedence over the file's `kntnt.language: en_US` and that the frontmatter was left alone; nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the explicit flag suppressed the map's contrary value, and the Swedish body was judged under Swedish mechanics.
  - `preserve` — `pass` — the frontmatter is byte-identical; the map still says `en_US`, because synchronising it is Redline's business and not this Skill's.
  - `status` — `pass` — the short status came back in the language of the Text Artifact.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the fixture's genre and technique conflicts are not this Skill's parameters, and neither was read or reported.

## `handoff-unusable`

- **fixture** — `handoff-unusable`
- **invocation** — `/proofread $RUN/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no correction: the reply reported unusable artifact metadata, named `en_UK`, said it is neither a canonical code nor an installed alias, listed what is installed, stated explicitly that it had not read it as `en_GB`, and offered the formal override and the document fix as the two ways on.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — the resemblance to `en_GB` was named and refused rather than acted on.
  - `refusal` — `pass` — the run stopped at the metadata, with nothing corrected and nothing written.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the discarded plugin run over this fixture proofread the file anyway and mentioned `en_UK` only as an aside, which is the behaviour this fixture was built to distinguish from.

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/proofread $RUN/corpus/frontmatter/frontmatter-unrelated.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status which named the four bait keys, said they are the document's own fields because no top-level `kntnt` map is present, and reported the language as English inferred from the body; nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — `lang: fr` and `language: Esperanto` were not read as configuration, and inference from the body decided the language.
  - `preserve` — `pass` — the frontmatter block is byte-identical, `genre: fiction` and `technique: montage` included.
  - `status` — `pass` — the short status rather than a repeated text.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/proofread $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a no-change status naming `en_GB`, inferred from `artefact` and `rota`; nothing written.
- **side effects** — none.
- **criteria** —
  - `language` — `pass` — inference decided the locale with no metadata of any kind present.
  - `preserve` — `pass` — no `kntnt` map was added to a file that had no frontmatter at all.
  - `status` — `pass` — the short status rather than a repeated text.
  - `effects` — `pass` — the inventory is identical before and after.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — no metadata was demanded and nothing was refused, which is the whole of what this baseline asks.

## `response-default`

- **fixture** — `response-default`
- **invocation** — `/proofread $RUN/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the reply itself; see the `frontmatter-absent` entry, which is the same run. The fixture has no material of its own and the corpus directs it to be run with `frontmatter-absent` or any prose fixture.
- **side effects** — none.
- **criteria** —
  - `target` — `pass` — with no destination named, the result stayed in the response.
  - `effects` — `pass` — nothing was created, replaced, or removed anywhere under the working copy by a run that named no destination.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the twelve other response-targeted runs in this record agree: not one of them wrote anything.

## `new-file`

- **fixture** — `new-file`
- **invocation** — `/proofread --output=$RUN/out/draft.md $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out/draft.md`
- **observed delivery** — the reply reported the corrected text written to the named path, listed the corrections, and said the source was untouched; the artifact was not also printed in full.
- **side effects** — `out/draft.md` created. Nothing else created, replaced, or removed.
- **criteria** —
  - `target` — `pass` — exactly the named path was created, and nowhere else was written.
  - `mechanics` — `pass` — the file's diff against the fixture carries the fourteen corrections and nothing else.
  - `preserve` — `pass` — that same diff shows no line changed for any reason but an error.
  - `effects` — `pass` — one file created, no partial file, and the source's hash is unchanged.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the file written here is byte-identical to what the in-place run produced for the same fixture, so the destination changes where the artifact goes and not what it says.

## `existing-file`

- **fixture** — `existing-file`
- **invocation** — `/proofread --output=$RUN/corpus/output/existing-target.md $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/existing-target.md`
- **observed delivery** — the reply said the existing file had been overwritten with the complete corrected text and listed the corrections.
- **side effects** — `corpus/output/existing-target.md` replaced. Nothing else created, replaced, or removed.
- **criteria** —
  - `target` — `pass` — the occupant text is gone and the corrected artifact is in its place, with no sibling written beside it and nothing asked for beyond the path itself.
  - `effects` — `pass` — the directory holds exactly the files it held before, and only the named one changed.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — no confirming flag was demanded, which is the fixture's own rejection: naming the exact existing path is the authorisation.

## `existing-directory`

- **fixture** — `existing-directory`
- **invocation** — `/proofread --output=$RUN/out $RUN/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the derived path it had written to and listed the corrections; the source was reported untouched.
- **side effects** — `out/flawed-en-US.md` created. Nothing else created, replaced, or removed.
- **criteria** —
  - `target` — `pass` — the filename was derived from the source basename with its `.md` extension retained, not from the directory, and the file landed inside the named directory.
  - `effects` — `pass` — one file created, and its content is byte-identical to what the same fixture produced at an explicit path.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/proofread --output=$RUN/corpus/output/collision $RUN/corpus/output/interview-notes.md`
- **contextual instruction** — `none`
- **output target** — `$RUN/corpus/output/collision`
- **observed delivery** — the reply reported no mechanical errors, named the two occupants it had stepped past, and said the complete text had gone to `interview-notes-3.md` because an explicitly named destination receives the artifact whether or not anything changed.
- **side effects** — `corpus/output/collision/interview-notes-3.md` created. Both occupants are byte-identical to the corpus originals.
- **criteria** —
  - `target` — `pass` — the stem stayed `interview-notes` and the first free candidate in ascending order was taken, rather than a suffix built on the colliding `interview-notes-2`.
  - `status` — `pass` — the unchanged result still reached the named directory, which is the half of the no-change rule that a directory target exercises.
  - `effects` — `pass` — one file created, neither occupant overwritten, and the source untouched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the written file is byte-identical to the source, which is the correct outcome for a clean text delivered to a chosen destination.

## `read-only-source`

- **fixture** — `read-only-source`
- **invocation** — `/proofread --in-place $RUN/corpus/output/readonly-source.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place, as requested
- **observed delivery** — a refusal: one line naming the file's `-r--r--r--` mode as the reason In-place Editing cannot apply, the `SYNOPSIS` section printed verbatim, a pointer to `/proofread --help`, and three ways on — the response form, an `--output` path, or `chmod u+w` first.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the refusal names the problem, prints the synopsis, and offers the alternatives without performing any of them.
  - `effects` — `pass` — the file's content and its mode are both unchanged; no permission was widened to make the write possible, and nothing was written anywhere else as a silent substitute.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the refusal came before the file was read for correction, so there was nothing half done to leave behind.

## `in-place-request`

- **fixture** — `in-place-request`
- **invocation** — `/proofread --in-place $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — the source file, in place
- **observed delivery** — a one-line status: no mechanical errors found, and the file was not rewritten.
- **side effects** — none.
- **criteria** —
  - `status` — `pass` — an in-place run that corrected nothing wrote nothing and said so, rather than rewriting the file with identical bytes.
  - `effects` — `pass` — the inventory is identical before and after, and no copy was left beside the source.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the writing half of In-place Editing is exercised by the `flawed-en-US` in-place entry above, this fixture's material being mechanically clean.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/proofread --output=$RUN/corpus/output/in-place-source.md $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — the source's own path, named as a separate output
- **observed delivery** — a refusal: one line saying `--output` names the same path as the input, that replacing a source has one name, the `SYNOPSIS` printed, and the `--in-place` invocation spelled out as the way to do what was asked.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the refusal names the problem and points at In-place Editing, which is the guidance the contract specifies for this case.
  - `effects` — `pass` — the file is unchanged and nothing was written anywhere.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/proofread --in-place --output=$RUN/out/copy.md $RUN/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — two, which is the point of the fixture
- **observed delivery** — a refusal: one line saying both were given and that they name two destinations for one text, the `SYNOPSIS` printed, and each of the two single-destination invocations spelled out.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the contradiction is named before anything is read for correction.
  - `effects` — `pass` — neither half was executed: the source is unchanged and `out/copy.md` does not exist.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `url-source` (In-place Editing refused)

- **fixture** — `url-source`
- **invocation** — `/proofread --in-place https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — in place, against a URL
- **observed delivery** — a refusal: one line saying In-place Editing requires a writable local file and that fetching a URL grants no right to write anything back, the `SYNOPSIS` printed, and the response form, an `--output` path, and a local copy offered as the ways on.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the refusal is made by reading the invocation, and the reply states that nothing was even fetched.
  - `effects` — `pass` — nothing was created anywhere under the working copy.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the fixture's own rejection for this Skill, and it holds.

## `url-source` (URL read, filename derived from it)

- **fixture** — `url-source`
- **invocation** — `/proofread --output=$RUN/out https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — `$RUN/out`
- **observed delivery** — the reply named the resolved language, the derived path it had written to, nine corrections, and the things it had deliberately left; the artifact was not also printed.
- **side effects** — `out/key-words-for-use-in-rfcs-to-indicate-requirement-levels.txt` created. Nothing else created, replaced, or removed.
- **criteria** —
  - `target` — `pass` — with no source basename to derive from, the filename came from the document's title and kept a suitable text extension, and the file landed inside the named directory.
  - `preserve` — `pass` — the file on disk keeps the RFC's fixed-width layout, its page furniture, and its normative keyword list; no definition was added to or taken from what the RFC gives.
  - `mechanics` — `pass` — the corrections are mechanical: a misspelling, a duplicated space, subject–verb agreement in the five numbered definitions, and two misplaced sentence periods.
  - `effects` — `pass` — one file created, and nothing under the working copy touched.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the run also changed the boilerplate *specifies an Internet Best Current Practices* to *Practice*. It is a number-agreement correction and the run named it as one; a reader who considers the phrase a formal designation rather than prose would want it left, and it is recorded here so that the GPT-family record can be compared on the same sentence.

## `in-place-request` (variant: inline text, no corpus fixture)

- **fixture** — `in-place-request`
- **invocation** — `/proofread --in-place The bug were not in the parsing at all, and we shipped anyway which I would defend but not recomend.`
- **contextual instruction** — `none`
- **output target** — in place, against inline text
- **observed delivery** — a refusal: one line saying `--in-place` requires a *PATH* and the text was supplied inline, so there is no file to replace, the `SYNOPSIS` printed, and the flagless form offered.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — the documented in-place refusal for inline text was made, and nothing was corrected on the way past it.
  - `effects` — `pass` — nothing was written anywhere.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus carries no fixture for this refusal; the ticket asks for every documented in-place refusal, so it was run with inline material of its own.

## `in-place-request` (variant: two Text Artifacts, no corpus fixture)

- **fixture** — `in-place-request`
- **invocation** — `/proofread --in-place $RUN/corpus/prose/flawed-en-US.md $RUN/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — in place, against two files
- **observed delivery** — a refusal: one line naming both files and saying the Skill proofreads exactly one text per invocation, the `SYNOPSIS` printed, and the advice to invoke it once per file.
- **side effects** — none.
- **criteria** —
  - `refusal` — `pass` — more than one Text Artifact was refused rather than resolved into a configuration per file.
  - `effects` — `pass` — neither file was read for correction and neither was changed, so the refusal left no partial effect on the first of the two.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the corpus carries no fixture for this refusal either; it is the last of the documented in-place refusals.

## `flawed-en-US` (model invocation, proofreading term)

- **fixture** — `flawed-en-US`
- **invocation** — none; the user's message was `Can you proofread this for me?` followed by the fixture's first two paragraphs pasted inline.
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Skill under evaluation started of its own accord, and the reply carried the corrected text, a list of the six corrections, and a note of what was left as valid.
- **side effects** — none.
- **criteria** —
  - `trigger` — `pass` — a specific text plus an explicit proofreading term started the Skill, with no routing hint of any kind supplied.
  - `mechanics` — `pass` — `writen`, `It's job`, `into into`, `wasnt`, `would of been`, and `The bug were` were all corrected in the pasted material.
  - `preserve` — `pass` — wording, tone, and structure came through unchanged.
  - `effects` — `pass` — nothing was written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — inline supply is exercised here as well as the trigger.

## `flawed-en-US` (model invocation, mechanical-only request)

- **fixture** — `flawed-en-US`
- **invocation** — none; the user's message was `Fix the spelling and grammar mistakes in this paragraph. Don't change anything else about it.` followed by the fixture's third paragraph pasted inline.
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Skill under evaluation started of its own accord and returned the corrected paragraph with its three corrections listed.
- **side effects** — none.
- **criteria** —
  - `trigger` — `pass` — a request unambiguously limited to mechanical language errors started the Skill without any proofreading term being used.
  - `mechanics` — `pass` — `writting`, `differences was`, and `dont` were corrected.
  - `no-drift` — `pass` — the closing clause the paragraph is built on was left exactly as written, and the reply says so.
  - `effects` — `pass` — nothing was written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — the reply names British English as the mechanics applied. The excerpt carries no locale marker, bare English resolves to the declared British default, and no locale-specific change was made either way; the full-file runs, where the text does carry markers, resolve `en_US`.

## `flawed-en-US` (model invocation withheld: improve)

- **fixture** — `flawed-en-US`
- **invocation** — none; the user's message was `Can you improve this paragraph for me?` followed by the fixture's third paragraph pasted inline.
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Skill under evaluation did not start. The turn was handled by an unrelated editing Skill, which rewrote the paragraph, split its last sentence, and explained the substantive changes.
- **side effects** — none.
- **criteria** —
  - `trigger` — `pass` — a generic request to improve did not start a Skill whose contract is limited to mechanics, which is what the description's exclusions promise.
  - `effects` — `pass` — nothing was written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — that the turn produced a rewrite is the correct outcome for the request; what matters here is that the rewrite did not come from this Skill.

## `flawed-en-US` (model invocation withheld: polish and tighten)

- **fixture** — `flawed-en-US`
- **invocation** — none; the user's message was `Please polish this and tighten it up a bit:` followed by the fixture's third paragraph pasted inline.
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Skill under evaluation did not start; an unrelated editing Skill tightened the paragraph and named its changes.
- **side effects** — none.
- **criteria** —
  - `trigger` — `pass` — polish and tighten are named exclusions, and neither started the Skill.
  - `effects` — `pass` — nothing was written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — none.

## `flawed-en-US` (model invocation withheld: review and edit)

- **fixture** — `flawed-en-US`
- **invocation** — none; the user's message was `Have a look at this and review it for me. Also feel free to edit it.` followed by the fixture's third paragraph pasted inline.
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the Skill under evaluation did not start; an unrelated editing Skill returned an edited draft and a review.
- **side effects** — none.
- **criteria** —
  - `trigger` — `pass` — review and edit together, on a specific text, still did not start a Skill contracted to mechanics.
  - `effects` — `pass` — nothing was written.
- **unresolved findings** — none.
- **defects filed** — none.
- **notes** — this is the hardest of the three withholding cases, because the message names a specific text and invites a change to it. The exclusion held.

## Fixtures deliberately skipped

Six fixtures were not run against this Skill. Each is recorded here rather than omitted, because a record silently missing a fixture reads later as a fixture that passed.

- `brief-short` — `skipped` — a brief for a draft. Proofread takes a Text Artifact to correct, not a brief to write from; the corpus's `Reject` line for it judges a draft's supported facts, which this Skill produces nothing to judge. Inline supply, the one thing it would additionally exercise, is exercised by the two model-invocation runs above.
- `brief-article-abt` — `skipped` — same reason; its rejections are about genre, technique, and attribution, none of which this Skill resolves.
- `brief-report-pac` — `skipped` — same reason.
- `brief-press-release-sv` — `skipped` — same reason. Swedish language inference, the part of it that could bear on this Skill, is exercised by `flawed-sv` and `handoff-conflicting`.
- `interview-transcript` — `skipped` — its rejections concern quotation fidelity in a draft that quotes the speaker, which is Write's invariant. Proofreading a transcript would exercise nothing this record does not already hold.
- `factual-source-long` — `skipped` — its rejections concern causal claims and figures in a draft made from it, which this Skill neither makes nor can make.

## Runs discarded

Ten by-name runs, driven before the plugin collision described under **Run conditions** was noticed, reached `kntnt-text-skills:proofread` instead of the Skill under evaluation. They are named here so that the count of turns spent is honest, and they carry no criteria: they say nothing about this Skill. Every fixture they touched was re-run from a fresh working copy against the right Skill, and it is those re-runs that this record holds. The behaviours differ visibly — the plugin edited files in place that no invocation had asked it to edit, changed an em dash in the clean fixture, and proofread the unusable-metadata fixture instead of reporting the metadata — which is why they could not be quietly kept.
