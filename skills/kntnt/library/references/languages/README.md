# Language Resources

This directory holds one Language Resource per supported language or locale, and this page is the format they are written to. Read it before adding a locale. The resolver beside it — `../../scripts/languages.py` — is what selects among them and what verifies that a new one is well formed.

A Language Resource is one Markdown file carrying everything about one language that an editorial Skill needs: the metadata that selects it, and the language-specific guidance a Skill loads once it has been selected. Adding a language is therefore writing one file here, never a coordinated edit across a registry, an alias table, and three Skills.

## The file

One file per language or locale, named for its canonical code with a `.md` extension — `sv.md`, `en_GB.md`, `en_US.md`. Identity comes from the frontmatter rather than from the filename, so the name is a convention for whoever reads the directory rather than something the resolver goes by; two files claiming one code are refused wherever they are named. This page is the only file here that is not a resource.

A file has YAML frontmatter between `---` delimiters, then a body. The frontmatter is read on its own whenever the resolver inventories what is installed, and the body is opened only when a caller asks for a scope out of it. Keep the frontmatter small for that reason: it is read every time, and the body is not.

## Frontmatter

**`code`** — required. The canonical code, written as `xx` for a language and `xx_YY` for a locale: a lowercase language subtag, an underscore, an uppercase territory subtag. British English is `en_GB`; no other spelling of it is a code or an alias anywhere here. A selector reaches this code whatever case and separator it is typed with, so `en-GB`, `EN_GB`, and `en gb` all arrive at the same resource, and the file itself is still written the canonical way.

**`language`** — required. The language's name in English, in one string: `Swedish`, `English`. It names the language, never the locale, so `en_GB` and `en_US` both carry `English`.

**`territory`** and **`territory-name`** — optional, and written together where a resource is a locale rather than a base language. The territory is the two-letter uppercase code, the name is that territory in English: `GB` and `United Kingdom`.

**`aliases`** — optional. A curated list of human names and abbreviations a person would actually type for this language: `british english`, `BrE`, `brittisk engelska`. Case and separators do not matter, so write each alias once in its natural form. At most twelve, because this is a curated set and not a multilingual registry — an unlisted description of a language is interpreted by the agent and then verified against what is installed, which is why exhaustiveness is not the goal. An alias that merely respells a canonical code is refused: the code already selects itself.

**`default-for`** — optional. The bare selectors this resource answers to when nothing more specific was asked for. `en_GB` carries `default-for: [en]`, which is the whole of why bare English is British English: the answer is declared by the resource that owns it rather than by a table somewhere else. Two resources declaring the same default make that selector ambiguous, and the resolver refuses it rather than picking one.

**`inherits`** — optional. The canonical code of the base language this locale falls back to for any scope it does not write itself. One step and no further: a base that inherits in turn, a base nothing installs, and a resource naming itself are all reported as inheritance errors rather than quietly flattened.

## The four scopes

The body carries four scopes, each introduced by its own second-level heading and each holding everything under it until the next one. Anything above the first heading is the resource's own introduction and belongs to no scope. Deeper headings inside a scope are that scope's own structure.

```
## Composition

## Review

## Anti-slop

## Mechanics
```

A caller asks for the scopes it can act on and is given those and no others, so the boundaries between them are what keep a Skill from paying for guidance it will not use. Each scope is named for what it holds rather than for the Skill that reads it: more than one Skill reads some of them, and a scope named after a consumer would read as that consumer's property.

**Composition** is for writing in the language: register, idiom, word order, the forms a fluent writer reaches for and the calques a translated draft falls into. It is written for an agent producing a first draft.

**Review** is language-specific editorial guidance: what to look for when reading a finished text in this language, which constructions read as bureaucratic or foreign here, and how to say the same thing more plainly in it. It is diagnostic, where composition is generative.

**Anti-slop** is the words, phrases, punctuation, and constructions that mark machine-sounding prose in this language specifically. The generic anti-slop patterns are shared and language-independent; what belongs here is what those patterns cannot see — a phrase that only exists in this language, a punctuation convention a generating model imports from English, a tell that a text was translated rather than written.

**Mechanics** is objective correctness in this language: spelling, inflection, agreement, punctuation, and locale conventions for dates, numbers, currency, and quotation. Nothing here may be a preference. Where two forms are both correct, say that both are established here and leave it there — what a Skill does about established variation is stated once for every language, in the shared mechanics contract beside this directory, and a scope that says it again is a second copy free to disagree with the first.

An objectively wrong punctuation form belongs in Mechanics even when its presence is also a language-specific generation tell. Anti-slop refers to that rule rather than restating it, so the form remains reachable to a mechanical pass and has one authoritative definition.

## What does not belong in a scope

Generic editorial rules stay out. A rule that is true of good writing in general belongs to the shared contract every Skill loads, and its English examples are applied semantically in the target language rather than translated into a copy here. So does a rule of objective correctness that holds in the same way in every language: it belongs to the shared mechanics contract, which a Skill correcting mechanics loads beside the scope, and a mechanics scope states only what its own language settles differently.

A rule enters a scope for one of two reasons only: the language genuinely differs, or the generic rule was observed to fail on this language. Anything else duplicates a rule that is already true somewhere else, and a rule written twice is a rule that can disagree with itself.

Keep the prose in English. Examples, word lists, and the mechanics of the language itself are written in the language, because that is what they are about; the explanation around them is not.

## Adding a locale

Write one file, give it the canonical code of the locale, declare `inherits` pointing at its base language, and write only the scopes that genuinely differ. A Finland Swedish resource inheriting from `sv` and overriding mechanics alone is a complete resource: the three scopes it does not write are answered by its base.

Then check it:

```
uv run skills/kntnt/library/scripts/languages.py validate
uv run skills/kntnt/library/scripts/languages.py resolve --scope=mechanics <code>
```

`validate` holds every installed resource to this page — the frontmatter vocabulary, the canonical spellings, the alias cap, the scope headings, the requirement that every resource can answer all four scopes itself or through its base, and that no two of them answer to the same selector. The filename convention is the one rule here it does not check. `resolve` is what a Skill actually calls, so running it once on the new code is what proves the resource is reachable by the selectors a person will type.
