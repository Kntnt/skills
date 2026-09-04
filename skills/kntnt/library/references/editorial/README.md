# Editorial resources

This directory holds the editorial contract the Collection's editorial Skills are written and reviewed against: [`base.md`](base.md), the genres under `genres/`, the techniques under `techniques/`, and [`anti-slop.md`](anti-slop.md) and [`mechanics.md`](mechanics.md) beside them. This page is the format they are written to. Read it before adding a genre or a technique, or before changing what the base contract, the anti-slop catalogue, or the mechanics contract holds.

Everything here is language-independent and written in English. The language-specific half lives beside it in [`../languages/`](../languages/README.md), one resource per language, and the two are loaded together at run time. A rule that is only true of one language belongs there and never here.

## The base contract

`base.md` holds every normative outcome a first draft is expected to meet. Every one of them, and each of them once: a Skill that writes and a Skill that reviews read the same document, so a requirement stated in two places is a requirement that can come to disagree with itself about what was required.

It states outcomes rather than procedure, and it names no Skill and no option. What differs between drafting and reviewing is what a Skill does about a failure, never what counts as one, so a contract that mentioned a flag would bind a grammar the consuming Skill owns.

Its examples are English and are meant to be applied semantically. An example demonstrates a pattern by what it does, and a reader applies it in the target language rather than looking for the English words in it. That is why the contract is not translated per language and must not grow a translated copy anywhere.

## Genres and techniques

A genre says what a kind of text owes its reader on top of the base contract: what a report, an article, or a press release is, and what a reader of one expects. A technique is a chosen structure for a text — an editorial requirement the draft has to satisfy, never a template to be filled in.

Part of what a kind of text owes its reader is the shape its reader expects, and where a genre has one the base half states it: which parts a text of this kind carries, and the order somebody meets them in. A reader who meets a kind of text often reads it by habit — they know where the next thing is and they find it there — so a text that rearranges the parts spends that recognition before its content gets a hearing. State the shape as every other requirement here is stated, as an outcome the draft has to reach rather than a procedure for reaching it: what the reader expects to find, and in what order. Never a numbered form to fill, and never a measurement bolted to a part — a word count, a character limit, a number of paragraphs — because what a reader recognises is the part and its place, and a measurement is a different rule wearing the shape's clothes.

A shape is stated where the genre has one, and is not invented for a genre that has none. The test is the reader: a convention whose absence they would notice is part of what the genre owes them, and a shape written here because the format allowed one is a convention this Collection invented and then imposed on every text of that kind afterwards. Where the structure is the writer's to choose from the material, the genre states no shape, and the base contract's ordering by the reader's need is the whole of it. `general` is the case that settles the boundary: the default genre imposes no convention at all, because a text whose kind nobody named has no reader expecting one.

One file per genre, in `genres/`, and one file per technique, in `techniques/`. The filename without its extension is the canonical value: `genres/general.md` is the genre `general`, and that is the spelling recorded in Handoff Metadata whatever the user typed. Use lowercase and hyphens, so a press release is `press-release.md`.

The directory is the list. Nothing enumerates the installed genres or techniques anywhere else, which is what keeps adding one a matter of writing one file: a Skill resolving a selection reads the directory, and a value with no file is refused rather than falling back to a default.

A resource opens with `# <Name>` and a first paragraph saying in one or two sentences what this genre or technique is, so that a Skill listing what is installed has something to show without loading the rest. That opening is also what a genre inferred rather than named is inferred against: a Skill settling an unnamed genre reads the directory listing and these openings, and nothing further of any resource it does not resolve. It is therefore a requirement on every resource rather than a courtesy — an opening that does not say what its genre is leaves a Skill choosing between them nothing but the filename, and the reading it would fall back on is the whole resource. Below that it states its requirements, and it states only what the base contract does not: a rule repeated here is one rule made into two things to keep true.

A genre's base half names the technique that genre is ordinarily written with, or states that it has none, and every genre in the directory states one or the other. That is a statement of practice rather than a requirement on the draft: a Skill's resolution order reads it below everything the user or the material says and above no technique at all, so somebody who names a kind of text and no technique gets the arc that kind of text ordinarily has, and somebody who names a technique gets the one they named. It is written as its own section below the requirements, where a run choosing between installed genres never reaches it — the openings are what an unnamed genre is settled against, and a technique named up there would be read as evidence about which genre this is.

`general` is the default genre and therefore the contract an unspecified content type gets in full. A technique applies because it was selected — by the person invoking, by the material's own metadata, by an instruction, or by the genre that was resolved — and nothing anywhere gives a Skill grounds to infer one from a draft's shape.

## Review extensions

Each of these documents has a base half and an optional review half, and the review half is a file of its own: `general.review.md` beside `general.md`, `base.review.md` beside `base.md`. A Skill that only writes loads the base half and stops; a Skill that reviews asks for the extension by name and gets it only when it exists.

The extension holds diagnostics, examples, edge cases, ambiguity resolution, and minimum-safe-correction guidance for the requirements its base half already states. It introduces no independent target — anything a draft has to meet is a base rule, and belongs in the base half where the writing Skill will actually see it — and it restates no base rule in other words, because a requirement and its diagnostic drift apart the moment both claim to say what is required.

The review half is written for the Skill that reviews, and it ships beside the base half whose requirements it diagnoses rather than waiting for that Skill to exist: diagnostics written later, by somebody reading the requirements from outside, are how a review acquires a target the writer was never given. Its absence is not a defect either — a base half with no extension beside it is a complete resource.

## The anti-slop catalogue

`anti-slop.md` is the collection's own condensed adaptation of the patterns that mark machine-sounding prose: what each looks like, what it costs the reader, and the smallest change that removes it. It sits here rather than under a Skill because more than one Skill applies that pass, and a copy under the first of them would make that Skill the owner of its peer's rules.

It is diagnostic throughout and states no target of its own. A Skill reading it beside the base contract meets nothing the contract does not already hold; a Skill contracted to apply that pass alone reads it without the contract and has what it needs. Its examples are English and semantic, like every other example here, and the words, phrases, punctuation, and constructions that only exist in one language belong to that language's own anti-slop scope.

Where it carries wording or a substantial portion of an upstream catalogue, the upstream notice ships inside the file, because a reader of an installed Skill receives the file and not this repository.

## The mechanics contract

`mechanics.md` holds the rules of objective correctness that do not depend on which language a text is in — today the clause boundary a comma may and may not carry, what each way of setting a quotation requires of the punctuation and capitalisation around it, the ordinary capitalisation of a spelled-out abbreviation, the one convention a list holds throughout, and the rule that where a language establishes more than one correct form the text's own choice stands. A Skill contracted to mechanical correction reads it together with the resolved language's mechanics scope, and the two together are that run's rules.

It sits here for the reason the anti-slop catalogue does: what is true of every installed language has to be written somewhere that is not one of them. Written once per language it would be one rule made into as many things to keep true, and the copies would be free to disagree about what is an error; written nowhere, a rule nobody states is decided by whoever is reading.

Nothing in it may be a preference, which is what separates it from the base contract beside it. The base contract holds what a first draft has to be, and a text can fail it and still be correct; this document holds what is wrong whatever the writer intended. A rule that turns on the language — spelling, inflection, agreement, a language's own punctuation, its conventions for dates, numbers, currency, and quotation — belongs to that language's resource, and the resource is the more specific instruction wherever the two meet. Otherwise it is written exactly as its siblings here are: outcomes rather than procedure, no Skill and no option named, and English examples applied semantically in the target language.

## Adding a genre or a technique

Write one file in the right directory, name it for the canonical value, and give it a base half. A genre's base half closes by naming the technique that genre is ordinarily written with, or by stating that it has none, which is the one statement here nothing else can supply for it. That section opens on the value itself — an installed technique's canonical name, or `none` — before whatever the genre says about why, because the suite reads the first word of it. Add the review extension beside it if there is diagnostic guidance to carry. Then check that a Skill can reach it: the value is the filename, so anything that reads the directory finds it without an edit anywhere else.
