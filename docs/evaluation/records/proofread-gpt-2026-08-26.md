- **record** — `proofread-gpt-2026-08-26`
- **date** — `2026-08-26`
- **ticket** — `#155`
- **skill** — `proofread`
- **provider family** — `gpt`
- **model** — `gpt-5.6-sol`
- **harness** — Codex CLI `0.149.1`
- **corpus commit** — `46ba9c1`

## `clean-en-GB`

- **fixture** — `clean-en-GB`
- **invocation** — `/proofread --language=en_GB /tmp/kntnt-gpt-eval.2WAfub/proofread-clean/corpus/prose/clean-en-GB.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The response was the short status “No changes were needed.” and did not repeat the artifact.
- **side effects** — `none`
- **criteria** —
  - `clean text` — `pass` — The run found no mechanical correction in the clean British English artifact.
  - `valid alternatives` — `pass` — The response indicates that `judgement`, `summarise`, `towards`, and the absent serial comma were left alone.
  - `unchanged response delivery` — `pass` — The run returned only the short no-change status.
  - `response side effects` — `pass` — The staged corpus and empty output directory were unchanged.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — The explicit invocation by name applied the mechanical-only contract.

## `flawed-en-US`

- **fixture** — `flawed-en-US`
- **invocation** — `/proofread --language=en_US /tmp/kntnt-gpt-eval.2WAfub/proofread-flawed-us/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The complete corrected artifact was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `complete mechanics` — `pass` — All staged spelling, contraction, duplicated-word, agreement, inflection, and sentence-boundary errors were corrected.
  - `locale mechanics` — `pass` — US spelling, unspaced em dashes, and punctuation inside double quotation marks were applied without British substitutions.
  - `clause boundary` — `pass` — The explanatory comma after “parsing at all” remained, while the unrelated March sentence was split at its joint.
  - `mechanical-only boundary` — `pass` — The wording, hedges, argument, paragraph structure, facts, and closing opinion were preserved.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `resembles-abt`

- **fixture** — `resembles-abt`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-resembles/corpus/prose/resembles-abt.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — A one-punctuation-change artifact was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `technique boundary` — `pass` — The run did not resolve, report, or impose ABT merely because the artifact resembled it.
  - `clean prose` — `fail` — A substantive edit from a mechanical-only pass inserted an optional comma after `Therefore`, although neither loaded mechanics resource names its absence as an error.
  - `unchanged response delivery` — `fail` — Because of the unsupported edit, the run repeated an artifact instead of returning the required short no-change status.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `#165`
- **notes** — `none`

## `mixed-language`

- **fixture** — `mixed-language`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-mixed/corpus/prose/mixed-language.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The run asked whether Swedish or English mechanics should apply and stated that no file had changed.
- **side effects** — `none`
- **criteria** —
  - `ambiguous language` — `pass` — Alternation inside paragraphs was recognized as materially mixed and produced one question rather than a guessed locale.
  - `pre-question side effects` — `pass` — The staged corpus and output directory remained unchanged.
- **unresolved findings** — Language selection remained unresolved pending the user’s answer.
- **defects filed** — `none`
- **notes** — The fixture intentionally ends at the required question.

## `locale-divergent` — British English

- **fixture** — `locale-divergent`
- **invocation** — `/proofread --language=en_GB /tmp/kntnt-gpt-eval.2WAfub/proofread-locale-gb/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — An artifact with one expanded date was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `British forms` — `pass` — `organised`, noun `licence`, the pound figure, and British quotation punctuation were preserved.
  - `ambiguous numeric date` — `fail` — An unsupported fact was introduced by expanding ambiguous `3/4` to `3 April` solely from the locale.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `#166`
- **notes** — `none`

## `locale-divergent` — American English

- **fixture** — `locale-divergent`
- **invocation** — `/proofread --language=en_US /tmp/kntnt-gpt-eval.2WAfub/proofread-locale-us/corpus/prose/locale-divergent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The complete US-localized artifact was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `American mechanics` — `pass` — American spelling, noun `license`, and period placement inside the quotation marks were applied.
  - `ambiguous numeric date` — `pass` — The source’s ambiguous `3/4` remained unchanged.
  - `fact preservation` — `pass` — The pound-denominated fact and all substantive content were preserved.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `handoff-present`

- **fixture** — `handoff-present`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-handoff-present/corpus/frontmatter/handoff-present.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — A British-mechanics artifact was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `metadata precedence` — `pass` — The `kntnt.language` value resolved exactly to `en_GB` without a language question.
  - `metadata preservation` — `pass` — The leading YAML block, including normalized genre, technique, and language values, was byte-for-byte unchanged.
  - `mechanics` — `pass` — The percentage was normalized under the resolved British mechanics scope and no broader editing occurred.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Genre and technique metadata were read past rather than applied.

## `handoff-conflicting`

- **fixture** — `handoff-conflicting`
- **invocation** — `/proofread --language=sv /tmp/kntnt-gpt-eval.2WAfub/proofread-handoff-conflicting/corpus/frontmatter/handoff-conflicting.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The response was the Swedish short no-change status; the artifact and source were not repeated or changed.
- **side effects** — `none`
- **criteria** —
  - `explicit precedence` — `pass` — `--language=sv` suppressed conflicting `kntnt.language: en_US` and the body’s Swedish mechanics governed the run.
  - `metadata preservation` — `pass` — Proofread’s immutable-metadata contract left the recognized map byte-for-byte unchanged despite the suppressed value.
  - `unchanged response delivery` — `pass` — The no-change status was short and written in Swedish.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Genre and technique are outside Proofread’s grammar and were not resolved.

## `handoff-partial`

- **fixture** — `handoff-partial`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-handoff-partial/corpus/frontmatter/handoff-partial.md -- Swedish is the language.`
- **contextual instruction** — `Swedish is the language.`
- **output target** — `response`
- **observed delivery** — The response was the Swedish short no-change status; the mixed artifact was not repeated.
- **side effects** — `none`
- **criteria** —
  - `context precedence` — `pass` — With no language flag or metadata value, the Contextual Instruction settled Swedish before ambiguous-text inference.
  - `partial metadata` — `pass` — The absent language key did not invalidate the recognized partial map, and its technique key was ignored but preserved.
  - `unchanged response delivery` — `pass` — The no-change status was short and written in Swedish.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `handoff-unusable`

- **fixture** — `handoff-unusable`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-handoff-unusable/corpus/frontmatter/handoff-unusable.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The run named `en_UK` as neither canonical nor an installed alias, stopped, and stated that nothing was written.
- **side effects** — `none`
- **criteria** —
  - `unusable metadata` — `pass` — `en_UK` was not silently reinterpreted as `en_GB`.
  - `refusal atomicity` — `pass` — No correction or filesystem effect preceded the refusal.
- **unresolved findings** — The artifact’s unusable language metadata remained for the caller to resolve.
- **defects filed** — `none`
- **notes** — `none`

## `frontmatter-unrelated`

- **fixture** — `frontmatter-unrelated`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-frontmatter-unrelated/corpus/frontmatter/frontmatter-unrelated.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The complete artifact with corrected question punctuation was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `configuration boundary` — `pass` — Top-level bait keys for language, genre, and technique were not read as Kntnt configuration.
  - `frontmatter preservation` — `pass` — The unrelated YAML block was byte-for-byte unchanged.
  - `mechanics` — `pass` — The missing question marks in the body’s quoted questions were corrected without broader edits.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Language was inferred from the body rather than the bait keys.

## `frontmatter-absent`

- **fixture** — `frontmatter-absent`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-frontmatter-absent/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The response was the short status “No mechanical corrections were needed.” and did not repeat the artifact.
- **side effects** — `none`
- **criteria** —
  - `metadata optionality` — `pass` — The run neither required nor added frontmatter or a Kntnt map.
  - `clean text` — `pass` — The mechanically clean artifact was left unchanged.
  - `response-default` — `pass` — The run returned only a short no-change status and changed nothing anywhere under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — This run also exercises the corpus’s `response-default` situation.

## `response-default`

- **fixture** — `response-default`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-frontmatter-absent/corpus/frontmatter/frontmatter-absent.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The response was the short no-change status and contained no repeated artifact.
- **side effects** — `none`
- **criteria** —
  - `default destination` — `pass` — No output option selected the response and no file was created, replaced, or removed anywhere under the staged working copy.
  - `unchanged result` — `pass` — The clean artifact produced only the short status.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — This is the same run as `frontmatter-absent`, recorded separately because `response-default` is a named output-situation fixture.

## `slop-heavy`

- **fixture** — `slop-heavy`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-slop-en/corpus/prose/slop-heavy.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The response was the short status “No mechanical corrections were needed.” and did not repeat the artifact.
- **side effects** — `none`
- **criteria** —
  - `mechanical-only boundary` — `pass` — The mechanically clean artifact’s anti-slop patterns were not treated as proofreading findings or rewritten.
  - `unchanged response delivery` — `pass` — The run returned only a short no-change status.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — Language was inferred from the artifact.

## `slop-heavy-sv` — inferred language

- **fixture** — `slop-heavy-sv`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-slop-sv-infer-iso/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — A mechanically corrected Swedish artifact was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `language inference` — `pass` — The run inferred Swedish and delivered Swedish text.
  - `locale mechanics` — `pass` — It corrected Swedish dash spacing, the connective-adverb comma, quotation marks, and the serial comma.
  - `mechanical-only boundary` — `pass` — Anti-slop content and `Service & support` were preserved.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — This replacement run was executed in an isolated workspace containing no historical evaluation records.

## `slop-heavy-sv` — explicit language

- **fixture** — `slop-heavy-sv`
- **invocation** — `/proofread --language=sv /tmp/kntnt-gpt-eval.2WAfub/proofread-slop-sv-explicit/corpus/prose/slop-heavy-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — A corrected Swedish artifact was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `explicit language` — `pass` — The explicit selector resolved Swedish and the delivery remained Swedish.
  - `locale mechanics` — `pass` — The staged Swedish punctuation and locale errors were corrected.
  - `mechanical-only boundary` — `fail` — A substantive edit from a mechanical-only pass changed `Service & support` to `Service och support`, although neither loaded mechanics resource names the ampersand as an error.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `#163`
- **notes** — The failure is preserved as the actual explicit-selector run outcome.

## `code-carrying-sv` — inferred language

- **fixture** — `code-carrying-sv`
- **invocation** — `/proofread /tmp/kntnt-gpt-eval.2WAfub/proofread-code-sv-infer/corpus/prose/code-carrying-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The corrected Swedish prose and unchanged code-bearing artifact were returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `language inference` — `pass` — Swedish was inferred and its mechanics scope applied.
  - `complete prose mechanics` — `pass` — The staged punctuation, `de`/`dem`, misspelling, split compound, duplicated word, and noun-number errors were corrected.
  - `code preservation` — `pass` — Diff inspection showed the fenced block, indented block, and inline code spans byte-for-byte unchanged.
  - `anti-slop boundary` — `pass` — The anti-slop patterns in ordinary prose were preserved.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `code-carrying-sv` — explicit language

- **fixture** — `code-carrying-sv`
- **invocation** — `/proofread --language=sv /tmp/kntnt-gpt-eval.2WAfub/proofread-code-sv-explicit/corpus/prose/code-carrying-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — A partly corrected Swedish artifact with unchanged code was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `explicit language` — `pass` — The explicit selector resolved Swedish and the delivery remained Swedish.
  - `complete prose mechanics` — `fail` — An unresolved mandatory finding remained: `olika bild` was delivered without the required noun-number agreement correction to `olika bilder`.
  - `code preservation` — `pass` — Diff inspection showed the fenced block, indented block, and inline code spans byte-for-byte unchanged.
  - `anti-slop boundary` — `pass` — The anti-slop patterns in ordinary prose were preserved.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — The unreported mechanical error `olika bild` remained in the delivered artifact.
- **defects filed** — `#164`
- **notes** — The failure is preserved as the actual explicit-selector run outcome.

## `flawed-sv`

- **fixture** — `flawed-sv`
- **invocation** — `/proofread --language=sv /tmp/kntnt-gpt-eval.2WAfub/proofread-flawed-sv/corpus/prose/flawed-sv.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The complete corrected Swedish artifact was returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `complete mechanics` — `pass` — The duplicated word, `dem`/`de`, misspelling, split compound, missing plural inflection, and missing idiom word were corrected.
  - `language-specific behavior` — `pass` — Delivery stayed in Swedish and the valid pronoun `hen` was preserved.
  - `mechanical-only boundary` — `pass` — The argument, wording, tone, structure, and figures were unchanged.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `code-carrying`

- **fixture** — `code-carrying`
- **invocation** — `/proofread --language=en_US /tmp/kntnt-gpt-eval.2WAfub/proofread-code-en/corpus/prose/code-carrying.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The corrected prose and unchanged code-bearing artifact were returned in the response; the source remained unchanged.
- **side effects** — `none`
- **criteria** —
  - `prose mechanics` — `pass` — The prose contraction, agreement, duplicated word, and US em-dash spacing errors were corrected.
  - `code preservation` — `pass` — Diff inspection showed the fenced block, indented block, and both inline code spans byte-for-byte unchanged, including bait misspellings and patterns.
  - `anti-slop boundary` — `pass` — The named anti-slop patterns in ordinary prose were not rewritten by the mechanical pass.
  - `response side effects` — `pass` — Filesystem comparison found no mutation under the staged working copy.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `new-file`

- **fixture** — `new-file`
- **invocation** — `/proofread --language=en_US --output=/tmp/kntnt-gpt-eval.2WAfub/proofread-new-file/out/draft.md /tmp/kntnt-gpt-eval.2WAfub/proofread-new-file/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `/tmp/kntnt-gpt-eval.2WAfub/proofread-new-file/out/draft.md`
- **observed delivery** — The response named the created file and did not repeat the artifact.
- **side effects** — Created exactly `/tmp/kntnt-gpt-eval.2WAfub/proofread-new-file/out/draft.md`.
- **criteria** —
  - `new file` — `pass` — The complete mechanically corrected artifact was written to the exact non-existing destination.
  - `single delivery` — `pass` — No sibling or directory was created, the source was unchanged, and the response contained only destination/status information.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `existing-file`

- **fixture** — `existing-file`
- **invocation** — `/proofread --language=en_US --output=/tmp/kntnt-gpt-eval.2WAfub/proofread-existing-file/corpus/output/existing-target.md /tmp/kntnt-gpt-eval.2WAfub/proofread-existing-file/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `/tmp/kntnt-gpt-eval.2WAfub/proofread-existing-file/corpus/output/existing-target.md`
- **observed delivery** — The response named the destination and reported no unresolved mechanics without repeating the artifact.
- **side effects** — Replaced exactly `/tmp/kntnt-gpt-eval.2WAfub/proofread-existing-file/corpus/output/existing-target.md`.
- **criteria** —
  - `existing file` — `pass` — The occupant was replaced with the complete corrected artifact without a second confirmation or a sibling file.
  - `source preservation` — `pass` — The source artifact remained unchanged.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — A failed internal patch attempt made no change before the successful atomic replacement.

## `existing-directory`

- **fixture** — `existing-directory`
- **invocation** — `/proofread --language=en_US --output=/tmp/kntnt-gpt-eval.2WAfub/proofread-existing-dir/out /tmp/kntnt-gpt-eval.2WAfub/proofread-existing-dir/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `/tmp/kntnt-gpt-eval.2WAfub/proofread-existing-dir/out`
- **observed delivery** — The response named the derived destination `flawed-en-US.md` without repeating the artifact.
- **side effects** — Created exactly `/tmp/kntnt-gpt-eval.2WAfub/proofread-existing-dir/out/flawed-en-US.md`.
- **criteria** —
  - `derived filename` — `pass` — The source basename and `.md` extension were retained inside the named directory.
  - `directory confinement` — `pass` — Nothing was written outside the named directory and the source remained unchanged.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `derived-name-collision`

- **fixture** — `derived-name-collision`
- **invocation** — `/proofread --language=en_GB --output=/tmp/kntnt-gpt-eval.2WAfub/proofread-collision/corpus/output/collision /tmp/kntnt-gpt-eval.2WAfub/proofread-collision/corpus/output/interview-notes.md`
- **contextual instruction** — `none`
- **output target** — `/tmp/kntnt-gpt-eval.2WAfub/proofread-collision/corpus/output/collision`
- **observed delivery** — The response named the derived destination `interview-notes-3.md` without repeating the artifact.
- **side effects** — Created `/tmp/kntnt-gpt-eval.2WAfub/proofread-collision/corpus/output/collision/interview-notes-3.md`; both occupants remained byte-identical.
- **criteria** —
  - `collision resolution` — `pass` — The first free ascending suffix was applied to the original stem and neither occupant was overwritten.
  - `content preservation` — `fail` — A substantive edit from a mechanical-only pass added quotation markup around the valid phrase `the word probably`.
- **unresolved findings** — `none`
- **defects filed** — `#169`
- **notes** — Filename behavior passed independently of the artifact-content failure.

## `read-only-source`

- **fixture** — `read-only-source`
- **invocation** — `/proofread --in-place /tmp/kntnt-gpt-eval.2WAfub/proofread-readonly/corpus/output/readonly-source.md`
- **contextual instruction** — `none`
- **output target** — in place
- **observed delivery** — The run refused the read-only source, printed the synopsis, and stated that no change was made.
- **side effects** — `none`
- **criteria** —
  - `read-only refusal` — `pass` — The permission remained `-r--r--r--`, the source bytes were unchanged, and no substitute output appeared.
  - `refusal atomicity` — `pass` — No partial file, sibling, permission change, or directory was left behind.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `in-place-request`

- **fixture** — `in-place-request`
- **invocation** — `/proofread --in-place /tmp/kntnt-gpt-eval.2WAfub/proofread-in-place/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — in place
- **observed delivery** — The response named the source path and reported one corrected comma splice without repeating the artifact.
- **side effects** — Replaced exactly `/tmp/kntnt-gpt-eval.2WAfub/proofread-in-place/corpus/output/in-place-source.md`.
- **criteria** —
  - `explicit authorization` — `pass` — The writable local source was replaced only after the formal `--in-place` request.
  - `minimal correction` — `pass` — The unrelated independent clauses were separated at their joint and nothing else changed.
  - `single destination` — `pass` — No copy or sibling was created.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — The before/after hash and modification time confirm an actual source replacement.

## `output-equals-source`

- **fixture** — `output-equals-source`
- **invocation** — `/proofread --output=/tmp/kntnt-gpt-eval.2WAfub/proofread-output-equals/corpus/output/in-place-source.md /tmp/kntnt-gpt-eval.2WAfub/proofread-output-equals/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — the source path
- **observed delivery** — The run refused the equal paths, directed the caller to `--in-place`, and printed the synopsis.
- **side effects** — `none`
- **criteria** —
  - `recognizable authorization` — `pass` — The source remained byte-identical and was not replaced through an output option.
  - `refusal atomicity` — `pass` — No file or directory was created, replaced, or removed.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `output-and-in-place`

- **fixture** — `output-and-in-place`
- **invocation** — `/proofread --output=/tmp/kntnt-gpt-eval.2WAfub/proofread-output-and-inplace/out/draft.md --in-place /tmp/kntnt-gpt-eval.2WAfub/proofread-output-and-inplace/corpus/output/in-place-source.md`
- **contextual instruction** — `none`
- **output target** — contradictory file and in-place targets
- **observed delivery** — The run refused the two destinations and printed the synopsis.
- **side effects** — `none`
- **criteria** —
  - `mutual exclusion` — `pass` — Neither the source nor the named output was written.
  - `refusal atomicity` — `pass` — No partial effect was left behind.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `url-source` — in-place refusal

- **fixture** — `url-source`
- **invocation** — `/proofread --in-place https://www.rfc-editor.org/rfc/rfc2119.txt`
- **contextual instruction** — `none`
- **output target** — in place
- **observed delivery** — The run refused In-place Editing for the URL before fetching or correcting it and printed the synopsis.
- **side effects** — `none`
- **criteria** —
  - `URL refusal` — `pass` — A URL was not treated as a writable local file and no substitute destination was used.
  - `refusal atomicity` — `pass` — The isolated working copy remained unchanged.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — No RFC definition was produced or attributed.

## `in-place-request` — inline refusal

- **fixture** — `in-place-request`
- **invocation** — `/proofread --in-place "This are inline text."`
- **contextual instruction** — `none`
- **output target** — in place
- **observed delivery** — The run refused In-place Editing for inline text and printed the synopsis.
- **side effects** — `none`
- **criteria** —
  - `inline refusal` — `pass` — Inline text was not treated as a writable file and was not corrected elsewhere.
  - `refusal atomicity` — `pass` — The isolated working copy remained unchanged.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — The corpus has no uploaded-source file, so the uploaded-source refusal is recorded below as skipped.

## `new-file` — missing parent refusal

- **fixture** — `new-file`
- **invocation** — `/proofread --output=/tmp/kntnt-gpt-eval.2WAfub/proofread-missing-parent/out/missing/draft.md /tmp/kntnt-gpt-eval.2WAfub/proofread-missing-parent/corpus/prose/flawed-en-US.md`
- **contextual instruction** — `none`
- **output target** — `/tmp/kntnt-gpt-eval.2WAfub/proofread-missing-parent/out/missing/draft.md`
- **observed delivery** — The run refused the missing parent directory and printed the synopsis.
- **side effects** — `none`
- **criteria** —
  - `unwritable destination` — `pass` — The parent was not created and no partial output was written.
  - `source preservation` — `pass` — The source remained byte-identical.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `flawed-en-US` — model trigger by proofreading term

- **fixture** — `flawed-en-US`
- **invocation** — `Proofread the specific text at /tmp/kntnt-gpt-eval.2WAfub/proofread-trigger-term/corpus/prose/flawed-en-US.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The Harness loaded Proofread and returned a mechanically corrected artifact in the response.
- **side effects** — `none`
- **criteria** —
  - `narrow trigger` — `pass` — A specific Text Artifact and explicit proofreading term fired the model-invocation trigger.
  - `same contract` — `pass` — The delivered artifact matched the explicit Skill run’s mechanical-only behavior.
  - `rule loading` — `fail` — The Harness trace shows language scopes outside mechanics were loaded during the model-invoked run.
- **unresolved findings** — `none`
- **defects filed** — `#170`
- **notes** — `none`

## `flawed-en-US` — model trigger by mechanical-only request

- **fixture** — `flawed-en-US`
- **invocation** — `Fix only the spelling, grammar, punctuation, agreement, inflection, duplicated-word, and missing-word errors in /tmp/kntnt-gpt-eval.2WAfub/proofread-trigger-mechanical/corpus/prose/flawed-en-US.md.`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — The Harness loaded Proofread and returned a mechanically corrected artifact in the response.
- **side effects** — `none`
- **criteria** —
  - `narrow trigger` — `pass` — A specific Text Artifact and unambiguous mechanical-only request fired the model-invocation trigger.
  - `same contract` — `pass` — The delivered artifact matched the explicit Skill run’s mechanical-only behavior.
  - `rule loading` — `fail` — The Harness trace shows language scopes outside mechanics were loaded during the model-invoked run.
- **unresolved findings** — `none`
- **defects filed** — `#170`
- **notes** — `none`

## `clean-en-GB` — generic polish request

- **fixture** — `clean-en-GB`
- **invocation** — `Polish the specific text at /tmp/kntnt-gpt-eval.2WAfub/proofread-trigger-polish/corpus/prose/clean-en-GB.md.`
- **contextual instruction** — `none`
- **output target** — outside Proofread
- **observed delivery** — The Harness explicitly declined to load Proofread and handled the broader edit as an ordinary polishing request.
- **side effects** — Replaced the isolated trigger copy’s source as part of the non-Proofread polish request.
- **criteria** —
  - `negative trigger` — `pass` — The generic term `polish` did not fire the narrow Proofread model-invocation trigger.
  - `contract separation` — `pass` — The Harness stated that polishing authorizes broader work than Proofread permits.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — The isolated copy’s mutation belongs to the ordinary polish request, not to a Proofread run, and is discarded with the temporary workspace.

## `brief-short` — skipped

- **fixture** — `brief-short`
- **invocation** — `skipped`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No run; the fixture is a Write source-fidelity brief rather than a pre-existing Text Artifact staged for a mechanical pass.
- **side effects** — `none`
- **criteria** —
  - `applicability` — `skipped` — Inline source-material composition is outside Proofread’s contract.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `brief-article-abt` — skipped

- **fixture** — `brief-article-abt`
- **invocation** — `skipped`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No run; the fixture evaluates Write’s genre, technique, and Source Fidelity behavior.
- **side effects** — `none`
- **criteria** —
  - `applicability` — `skipped` — Genre- and technique-selected composition is outside Proofread’s contract.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `brief-report-pac` — skipped

- **fixture** — `brief-report-pac`
- **invocation** — `skipped`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No run; the fixture evaluates Write’s report, PAC, and Source Fidelity behavior.
- **side effects** — `none`
- **criteria** —
  - `applicability` — `skipped` — Source-material composition is outside Proofread’s contract.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `brief-press-release-sv` — skipped

- **fixture** — `brief-press-release-sv`
- **invocation** — `skipped`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No run; the fixture evaluates Write’s inferred and explicit target-language composition.
- **side effects** — `none`
- **criteria** —
  - `applicability` — `skipped` — Press-release drafting is outside Proofread’s contract.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `interview-transcript` — skipped

- **fixture** — `interview-transcript`
- **invocation** — `skipped`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No run; the fixture evaluates Write’s quotation fidelity from source material.
- **side effects** — `none`
- **criteria** —
  - `applicability` — `skipped` — Drafting or repairing interview quotations is outside Proofread’s mechanical-only contract.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `factual-source-long` — skipped

- **fixture** — `factual-source-long`
- **invocation** — `skipped`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — No run; the fixture evaluates Write’s Source Fidelity against long source material.
- **side effects** — `none`
- **criteria** —
  - `applicability` — `skipped` — Source-to-draft fact selection is outside Proofread’s contract.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — `none`

## `uploaded-source` — skipped

- **fixture** — `uploaded-source`
- **invocation** — `skipped`
- **contextual instruction** — `none`
- **output target** — in place
- **observed delivery** — No run; Codex CLI `exec` exposes local paths, inline text, and URLs but no uploaded-source operand.
- **side effects** — `none`
- **criteria** —
  - `uploaded-source refusal` — `skipped` — The Harness provided no upload seam in this non-interactive evaluation; read-only, inline, and URL refusals were all exercised.
- **unresolved findings** — `none`
- **defects filed** — `none`
- **notes** — This is a documented delivery refusal rather than a named corpus file.
