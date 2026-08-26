# The fixture corpus

One body of material, shared by every evaluation of the editorial Skills, and readable on its own. Each fixture below says what the material is, how it reaches a Skill, and what a correct run must never do with it, so that an evaluator can use a fixture without first reading the Skill that consumes it.

The corpus is representative rather than exhaustive. It is fixture material, not a test suite: nothing here is an assertion about a sentence a model has to write back, and nothing here claims that any model writes perfectly or finds every error. What it does hold is the material the Skills are expected to survive, and the situations their output contract distinguishes.

The protocol that says how a run against this corpus is judged and recorded is in [`../protocol.md`](../protocol.md). Read it before running anything: it also carries the provider-isolation rule, which binds whoever runs an evaluation.

## Staging a run

A run mutates files, and the corpus is not the place for that. Take a working copy first, run against the copy, and throw the copy away afterwards:

```
WORK=$(mktemp -d)
cp -R docs/evaluation/corpus "$WORK/corpus"
mkdir -p "$WORK/out"
chmod a-w "$WORK/corpus/output/readonly-source.md"
```

That is the whole of the setup. `$WORK/out` is the empty existing directory the directory-output fixtures use; `chmod a-w` supplies the read-only source, which git cannot carry as a stored permission. Restore write permission before deleting the copy if your temporary directory refuses to remove a read-only file.

Record the corpus commit — `git rev-parse --short HEAD` in this repository — in every record. Two families comparing their runs are comparing runs against the same material only if both name the same commit.

## How a fixture entry reads

- **Files** — the corpus-relative paths the fixture consists of, or `none` where the fixture is a situation rather than material.
- **Covers** — the kinds of material or situation the fixture supplies, separated by semicolons.
- **Material** — what the text actually is.
- **Use** — how it reaches the Skill.
- **Reject** — what a correct run must never do with it, whatever wording it chooses.

A `Reject` line is a floor, not a rubric. The full judging criteria are the protocol's.

## Source material

### `brief-short`

- **Files** — `source/brief-short.md`
- **Covers** — short brief; inline material
- **Material** — a direct brief of about a hundred words: an audience, a length, five facts about a meeting that was replaced by a written update, and one explicit non-measurement.
- **Use** — paste the text into the invocation as inline material rather than naming the file, so that inline supply is exercised at least once.
- **Reject** — a draft that reports a benefit the brief does not contain. The brief says nobody asked to go back and says nothing shipped faster; a claim that the change made the team faster is unsupported.

### `brief-article-abt`

- **Files** — `source/brief-article-abt.md`
- **Covers** — genre; technique; local file material
- **Material** — a brief for a trade-publication article about ending a shared support inbox, with dated events, a counted defect, one named attributed quotation, and two stated limits.
- **Use** — supply the file path, and select the article genre and the ABT technique on the invocation.
- **Reject** — a draft that attributes to Miriam Adler anything she is not quoted as saying, that drops the two stated limits while asserting the result generalises, or that a reader could not recognise as the selected genre and technique.

### `brief-report-pac`

- **Files** — `source/brief-report-pac.md`
- **Covers** — genre; technique
- **Material** — a brief for an internal budget report on a second monitoring service, holding costs, coverage counts, a twelve-month alert history, an access-log fact, and a stated counter-argument.
- **Use** — supply the file path, and select the report genre and the PAC technique on the invocation.
- **Reject** — a draft that resolves the counter-argument by inventing evidence for or against it. Nothing in the material says whether independent failure has ever mattered here, beyond the sentence that no monitoring outage has occurred.

### `brief-press-release-sv`

- **Files** — `source/brief-press-release-sv.md`
- **Covers** — genre
- **Material** — a Swedish brief for a press release about a library repair workshop, with a date, opening hours, a funding figure, a named source, and two explicit exclusions.
- **Use** — supply the file path with the press-release genre selected, and let the language fall through to inference on one run and be named explicitly on another.
- **Reject** — a draft in any language but Swedish when nothing overrode inference, and any suggestion that the workshop repairs devices for visitors or sells parts, both of which the brief excludes.

### `interview-transcript`

- **Files** — `source/interview-transcript.md`
- **Covers** — interview transcript; local file material
- **Material** — a transcript of spoken answers with fillers, self-interruption, repetition, a self-correction about a number, and broken syntax throughout.
- **Use** — supply it as source material for a draft that quotes the speaker.
- **Reject** — a direct quotation that adds information the speaker did not give, changes her stance or her certainty, removes her self-correction from eleven-plus-others to eleven, or smooths away her distinctive wording while still presenting the result inside quotation marks. Where fidelity is doubtful, a paraphrase is the correct move and a fluent invented quotation is not. Source Fidelity also rejects calling the eleven full services *high*, *low*, *modest*, or otherwise relative: the material supplies no comparison, target, capacity, or speaker assessment of scale. The count remains eleven full services with the shorter jobs excluded, preserving the speaker's correction without classifying its size.

### `factual-source-long`

- **Files** — `source/factual-source-long.md`
- **Covers** — long factual source
- **Material** — an invented municipal evaluation of a bus route: roughly eight hundred words of dated decisions, boarding counts, a revenue and subsidy split the source itself calls an estimate, a survey with an eighteen per cent response rate and its own stated caveat, complaint counts, and a closing section listing the limits of the material. Nothing in it describes a real municipality, service, or person.
- **Use** — supply the file path as the single source for a draft of any genre.
- **Reject** — a causal claim about any one of the three simultaneous changes, a satisfaction figure quoted as a figure for the catchment, the seventeen missing counting days presented as zero boardings, or any number that is not in the source. The material contradicts each of these in its own text.

### `url-source`

- **Files** — `source/url-source.md`
- **Covers** — immutable url
- **Material** — a pointer file naming <https://www.rfc-editor.org/rfc/rfc2119.txt> as the source, with the brief that goes with it. RFC 2119 is a published RFC and the series does not revise published documents, so the material cannot move between two families' runs.
- **Use** — supply the URL as the source material. It is also the fixture for deriving an output filename from a URL rather than from a source basename.
- **Reject** — In-place Editing accepted against it, and any definition attributed to the RFC that the RFC does not give.

## Prose

### `clean-en-GB`

- **Files** — `prose/clean-en-GB.md`
- **Covers** — clean prose; no-change status; locale mechanics
- **Material** — four paragraphs of mechanically clean British English about handover documents, deliberately carrying valid forms an American-leaning reader is tempted to change: `judgement`, `summarise`, `towards`, `fortnight`, and no serial comma.
- **Use** — the fixture for a mechanical pass that should find nothing, and for a review that should not be tempted into rewriting competent prose.
- **Reject** — any change at all from a Skill contracted to mechanics, including the tempting ones; and a repeated full text where the contract asks for a short no-change status instead.

### `flawed-en-US`

- **Files** — `prose/flawed-en-US.md`
- **Covers** — mechanically flawed prose; locale mechanics; sentence-boundary punctuation
- **Material** — American English prose about rewriting an importer, carrying misspellings, a possessive-for-contraction error, a duplicated word, missing apostrophes, `would of`, two subject-verb disagreements, a missing plural, and two commas joining main clauses: one in *The bug were not in the parsing at all, it was in a silent retry* where the second clause explains the first, and one in *We finished in March, the finance team got a new reporting tool the same month* where the two clauses are unrelated.
- **Use** — the main fixture for complete mechanical correction, for the boundary between correcting and rewriting, and for the clause boundary a comma may and may not carry, which the fixture stages in both directions.
- **Reject** — American spellings changed to British ones, sentences restructured, hedges added or removed, or the closing opinion softened. The comma before *it was in a silent retry* is established usage in both shipped languages and is rejected as a correction; the unrelated pair is an error, and correcting it anywhere but at the joint — reordering the clauses, merging them, or supplying a conjunction rather than replacing the comma with a period or a semicolon — is rejected as well. Correcting the mechanics is the whole of the job.

### `flawed-sv`

- **Files** — `prose/flawed-sv.md`
- **Covers** — mechanically flawed prose
- **Material** — Swedish prose about abandoning a throughput metric, carrying a `de`/`dem` error, a compound written apart, a duplicated word, a misspelling, and a missing word in an idiom.
- **Use** — the fixture that shows whether mechanical correction is language-specific in practice rather than only in the contract.
- **Reject** — an English answer, a correction that changes the argument, and the informal `hen` replaced by anything else — it is a valid Swedish pronoun and not an error.

### `slop-heavy`

- **Files** — `prose/slop-heavy.md`
- **Covers** — ai slop
- **Material** — an essay about asynchronous communication carrying the patterns in concentration: an empty opening, false contrasts of the *it's not X — it's Y* shape, importance inflation, vague attribution to studies and experts, synonym cycling, a paragraph of identical short sentences, and a conclusion that restates the opening as a rhetorical question.
- **Use** — the fixture for anti-slop review, and for the difference between a review that names patterns and one that only dislikes the text.
- **Reject** — a review that finds nothing, a correction that removes the patterns and the content with them, and findings phrased as style preference where the pattern has a name.

### `slop-heavy-sv`

- **Files** — `prose/slop-heavy-sv.md`
- **Covers** — ai slop; swedish ai slop
- **Material** — a Swedish essay about digital customer service carrying the patterns in concentration, the way `slop-heavy` carries the English ones, and beside them the items the Swedish anti-slop scope names that English has no counterpart for: the Swedish empty openings and closings, the imported false contrast, the Swedish metaphor stock, superlative inflation, a comma after a fronted connective adverb where Swedish takes none, English punctuation carried across — the em dash, curly English quotation marks, a serial comma inside a Swedish list, and `&` standing in for *och* — the triad reflex, wholesale-translated hedging, and authority attributed to nobody.
- **Use** — the fixture for anti-slop review in Swedish. Supply the file path, with the language left to inference on one run and named explicitly on another. The shared catalogue is English and is applied by what each pattern does rather than by its words, so this is where that claim and the language's own scope are exercised in a language the catalogue is not written in.
- **Reject** — a review that finds nothing in a text built out of the patterns, an answer in any language but Swedish or a text rewritten into English, findings phrased as style preference where the pattern has a name, and a correction that removes the patterns and the content with them.

### `code-carrying`

- **Files** — `prose/code-carrying.md`
- **Covers** — code; ai slop; mechanically flawed prose
- **Material** — an article about kill switches whose prose carries the catalogue's patterns and three mechanical errors of its own — `Its` for *It's*, a subject-verb disagreement, and a duplicated word — wrapped around code the prose does not concern: a fenced JavaScript block, an indented block, and two inline code spans. The code is baited on both layers too: the comment, the docstring and the thrown message carry the same patterns as the article around them, two identifiers are named after patterns a pass is hunting, and two mechanical errors sit inside it — `recieved`, in a thrown message and again in an inline span naming a field, and `seperate`, in the indented block's comment.
- **Use** — supply the file path to any of the editorial passes. A run that changes nothing shows nothing here, so this is the fixture for a pass that does change the text: the prose earns findings on both layers, and the code is what has to survive them.
- **Reject** — a finding located inside a code sample, and code that does not come back byte for byte: the docstring's or the comments' patterns rewritten, either misspelling corrected, an identifier renamed, or an inline span edited. A sample is quoted material in all three of its forms, which [ADR-0125](../../adr/0125-a-code-sample-is-quoted-material-and-produces-no-findings.md) settles. Prose *about* code is ordinary prose, so the article's own mechanical errors are a mechanical pass's to correct and an anti-slop pass's to leave alone, and the patterns in its sentences are the reverse.

### `code-carrying-sv`

- **Files** — `prose/code-carrying-sv.md`
- **Covers** — code; ai slop; mechanically flawed prose
- **Material** — the Swedish counterpart on the same subject, whose prose carries the Swedish patterns and four mechanical errors of its own — a `de`/`dem` error, a misspelling, a compound written apart, and a duplicated word — around a fenced Python block, an indented block, and two inline code spans. The comment, the docstring and the raised message are Swedish and carry the same patterns as the article; inside the code sit `emmot` in a string literal and `seperat uppdaterings loop` in a comment, a misspelling and a compound written apart that are somebody's program rather than somebody's prose, and one inline span names a field misspelled the same way.
- **Use** — supply the file path, with the language left to inference on one run and named explicitly on another. It exists for the reason `slop-heavy-sv` does: a rule stated in English and exercised only in English has not been shown to reach the other shipped language, and a mechanical pass tempted by a misspelling is tempted in whatever language it reads.
- **Reject** — a finding located inside a code sample, and code that does not come back byte for byte: `emmot` corrected, the compound in the comment joined, the docstring's patterns rewritten, an identifier renamed, or an inline span edited. Prose *about* code is ordinary prose, so the article's own four mechanical errors are a mechanical pass's to correct in Swedish and an anti-slop pass's to leave alone.

### `resembles-abt`

- **Files** — `prose/resembles-abt.md`
- **Covers** — technique; clean prose
- **Material** — a competent account of adding a second server which happens to fall into an and-but-therefore shape, and even uses the word *therefore* to open its third paragraph.
- **Use** — supply it with no technique selected. It is the fixture for the rule that a technique applies because it was selected, not because the text resembles it.
- **Reject** — a resolved technique of ABT reported, recorded in metadata, or acted on when nothing selected it.

### `mixed-language`

- **Files** — `prose/mixed-language.md`
- **Covers** — ambiguous language
- **Material** — retrospective notes alternating between Swedish and English within paragraphs, with neither language dominant.
- **Use** — supply it with no language named, so that inference has to face material it cannot settle.
- **Reject** — a language silently picked and acted on. Material this mixed is a case for asking rather than guessing.

### `locale-divergent`

- **Files** — `prose/locale-divergent.md`
- **Covers** — locale mechanics; clean prose
- **Material** — a note whose mechanics diverge between British and American conventions: `organised`, `licence` as a noun, a pound figure, a numeric date written `3/4`, and quotation marks placed outside a final full stop.
- **Use** — run it under each English locale in turn to see whether the resolved locale reaches the mechanics.
- **Reject** — the ambiguous numeric date rewritten into an unambiguous one on the assumption of a locale, and British forms treated as errors where British English is the resolved locale.

## Frontmatter

### `handoff-present`

- **Files** — `frontmatter/handoff-present.md`
- **Covers** — handoff metadata present
- **Material** — a Text Artifact whose leading YAML carries a Kntnt map of `genre: article`, `technique: abt`, `language: en_GB`, matching the English body.
- **Use** — invoke with no genre, technique, or language named, so that all three fall through to the metadata.
- **Reject** — the map ignored, and the map's values reported back in a spelling other than the normalized ones it carries.

### `handoff-conflicting`

- **Files** — `frontmatter/handoff-conflicting.md`
- **Covers** — handoff metadata conflicting
- **Material** — a Swedish Text Artifact whose Kntnt map says `genre: report`, `technique: pac`, `language: en_US`, contradicting both the body and the invocation below.
- **Use** — invoke naming the Swedish language and the article genre, and naming no technique. Genre and language are then settled by the invocation, and only the technique falls through to the map.
- **Reject** — a metadata value overriding an explicit one, an explicit value for one parameter suppressing the map for the other two, and the file delivered with a Kntnt map still contradicting the configuration the run actually resolved. Source Fidelity rejects converting the before-and-after chronology into causality: both a causal verb and a causal hedge add an attribution the material does not support. The title, summary, and body obey the same boundary and preserve sequence without claiming that the new channel shortened the response time.

### `handoff-partial`

- **Files** — `frontmatter/handoff-partial.md`
- **Covers** — partial handoff metadata; ambiguous language
- **Material** — a Text Artifact whose Kntnt map carries `technique: abt` and neither of the other two keys, over a note about a newsletter that alternates Swedish and English inside its paragraphs, so that nothing in the artifact settles a language on its own.
- **Use** — invoke naming the report genre, no technique, and no language, with a Contextual Instruction naming Swedish as the language. Each of the first three levels of the resolution order then settles one parameter in a single run: the invocation settles the genre, the map settles the technique, and the Contextual Instruction settles the language the map leaves absent and the text cannot supply. It is the fixture for per-field resolution across all three at once, which a complete map makes unstageable.
- **Reject** — the two absent keys read as a reason to stop, to ask for a complete map, or to treat the map as unusable metadata; the technique taken from anywhere but the map, or refused because the map is incomplete; a language question asked where the Contextual Instruction has already named one; and the file delivered with a Kntnt map contradicting the configuration the run actually resolved.

### `handoff-unusable`

- **Files** — `frontmatter/handoff-unusable.md`
- **Covers** — unusable metadata
- **Material** — a Text Artifact whose Kntnt map names `language: en_UK`, a code the Collection does not carry and does not accept as an alias for British English.
- **Use** — invoke with no language named, so that nothing of higher precedence suppresses the unusable value.
- **Reject** — `en_UK` quietly read as `en_GB`, and the run continuing as though the metadata had been usable.

### `frontmatter-unrelated`

- **Files** — `frontmatter/frontmatter-unrelated.md`
- **Covers** — unrelated frontmatter
- **Material** — a Text Artifact with ordinary document frontmatter — title, layout, date, tags, draft — and, sitting among them at the top level, the bait keys `lang: fr`, `genre: fiction`, `technique: montage`, and `language: Esperanto`. No Kntnt map is present.
- **Use** — invoke with nothing named and let every parameter fall through.
- **Reject** — any of the four bait keys read as configuration, and any change to the frontmatter block by a Skill contracted to preserve it.

### `frontmatter-absent`

- **Files** — `frontmatter/frontmatter-absent.md`
- **Covers** — no frontmatter
- **Material** — a Text Artifact that opens directly on its heading, with no leading YAML of any kind.
- **Use** — the baseline case: every editorial Skill remains usable when no metadata exists.
- **Reject** — a demand for metadata, a refusal, and a Kntnt map added by a Skill that was not asked to write one.

## Output situations

### `response-default`

- **Files** — none
- **Covers** — response default
- **Material** — no material of its own; run it with `frontmatter-absent` or any prose fixture.
- **Use** — invoke with no output named at all, from the working copy, and take a before-and-after filesystem inventory of the whole staged working copy and the separate Harness scratch area rather than inspecting only the supplied material's directory.
- **Reject** — any file created, replaced, or removed in every writable location in the evaluation workspace by a run that named no destination, including a working copy of the artifact left in Harness scratch.

### `new-file`

- **Files** — none
- **Covers** — new file
- **Material** — no material of its own; the destination is a path that does not exist, such as `$WORK/out/draft.md`.
- **Use** — invoke naming that path as the output.
- **Reject** — a run that writes somewhere else, that creates the file and also prints the whole artifact as though no destination had been given, or that leaves a partial file behind after failing.

### `existing-file`

- **Files** — `output/existing-target.md`
- **Covers** — existing file
- **Material** — an occupant file whose text is visibly an occupant, so that a replacement is unmistakable.
- **Use** — invoke naming `$WORK/corpus/output/existing-target.md` as the output.
- **Reject** — a demand for an extra confirming flag, a sibling written beside it, and the occupant left in place while the result went elsewhere. Naming the exact existing path is the authorisation.

### `existing-directory`

- **Files** — none
- **Covers** — existing directory
- **Material** — the empty `$WORK/out` directory the staging step creates.
- **Use** — invoke naming the directory as the output, with a source whose basename or working title a filename can be derived from.
- **Reject** — a file named for the directory rather than derived from the source, a derived name with no suitable text extension, and anything written outside the named directory.

### `derived-name-collision`

- **Files** — `output/interview-notes.md`, `output/collision/interview-notes.md`, `output/collision/interview-notes-2.md`
- **Covers** — derived-name collision; existing directory
- **Material** — a source named `interview-notes.md`, and a directory that already holds `interview-notes.md` and `interview-notes-2.md`, both of them visibly occupants.
- **Use** — supply `$WORK/corpus/output/interview-notes.md` as the source and `$WORK/corpus/output/collision` as the output directory.
- **Reject** — either occupant overwritten; a name built by suffixing the colliding candidate rather than the original stem; and any change to the source wording or formatting, including quotation marks or other emphasis added around `probably`. The stem stays `interview-notes`, the first free candidate in ascending order is the one taken, and `interview-notes-3.md` otherwise matches the source.

### `read-only-source`

- **Files** — `output/readonly-source.md`
- **Covers** — read-only source; refusal
- **Material** — an ordinary Text Artifact, made read-only by the staging step.
- **Use** — request In-place Editing against it.
- **Reject** — a permission changed to make the write possible, a result written elsewhere as a silent substitute for the refusal, and a refusal that leaves any partial effect behind. The refusal itself is the correct outcome, and it names the problem.

### `in-place-request`

- **Files** — `output/in-place-source.md`
- **Covers** — in-place request
- **Material** — a writable local Text Artifact, the one case In-place Editing is available for.
- **Use** — request In-place Editing explicitly, with no separate output named.
- **Reject** — the source replaced without the explicit request, a copy left beside it, and a rewritten file where the run found nothing to change and a short status was the contract.

### `output-equals-source`

- **Files** — none
- **Covers** — refusal
- **Material** — no material of its own; use `in-place-request`'s file as both source and named output.
- **Use** — invoke naming `$WORK/corpus/output/in-place-source.md` as the source and the same path as the output.
- **Reject** — the file replaced. Source replacement has one recognisable authorisation, so this is refused and the refusal points at In-place Editing.

### `output-and-in-place`

- **Files** — none
- **Covers** — refusal
- **Material** — no material of its own; use `in-place-request`'s file with both an output path and In-place Editing requested at once.
- **Use** — invoke with both, in either order.
- **Reject** — either half executed. The two are mutually exclusive, and a contradictory request produces no side effect at all before it is refused.
