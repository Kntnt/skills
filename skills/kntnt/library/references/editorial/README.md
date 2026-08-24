# Editorial resources

This directory holds the editorial contract the Collection's editorial Skills are written and reviewed against: [`base.md`](base.md), the genres under `genres/`, and the techniques under `techniques/`. This page is the format they are written to. Read it before adding a genre or a technique, or before changing what the base contract holds.

Everything here is language-independent and written in English. The language-specific half lives beside it in [`../languages/`](../languages/README.md), one resource per language, and the two are loaded together at run time. A rule that is only true of one language belongs there and never here.

## The base contract

`base.md` holds every normative outcome a first draft is expected to meet. Every one of them, and each of them once: a Skill that writes and a Skill that reviews read the same document, so a requirement stated in two places is a requirement that can come to disagree with itself about what was required.

It states outcomes rather than procedure, and it names no Skill and no option. What differs between drafting and reviewing is what a Skill does about a failure, never what counts as one, so a contract that mentioned a flag would bind a grammar the consuming Skill owns.

Its examples are English and are meant to be applied semantically. An example demonstrates a pattern by what it does, and a reader applies it in the target language rather than looking for the English words in it. That is why the contract is not translated per language and must not grow a translated copy anywhere.

## Genres and techniques

A genre says what a kind of text owes its reader on top of the base contract: what a report, an article, or a press release is, and what a reader of one expects. A technique is a chosen structure for a text — an editorial requirement the draft has to satisfy, never a template to be filled in.

One file per genre, in `genres/`, and one file per technique, in `techniques/`. The filename without its extension is the canonical value: `genres/general.md` is the genre `general`, and that is the spelling recorded in Handoff Metadata whatever the user typed. Use lowercase and hyphens, so a press release is `press-release.md`.

The directory is the list. Nothing enumerates the installed genres or techniques anywhere else, which is what keeps adding one a matter of writing one file: a Skill resolving a selection reads the directory, and a value with no file is refused rather than falling back to a default.

A resource opens with `# <Name>` and a first paragraph saying in one or two sentences what this genre or technique is, so that a Skill listing what is installed has something to show without loading the rest. Below that it states its requirements, and it states only what the base contract does not: a rule repeated here is one rule made into two things to keep true.

`general` is the default genre and therefore the contract an unspecified content type gets in full. There is no default technique: a technique applies because it was selected, and nothing anywhere gives a Skill grounds to infer one from a draft's shape.

## Review extensions

Each of these documents has a base half and an optional review half, and the review half is a file of its own: `general.review.md` beside `general.md`, `base.review.md` beside `base.md`. A Skill that only writes loads the base half and stops; a Skill that reviews asks for the extension by name and gets it only when it exists.

The extension holds diagnostics, examples, edge cases, ambiguity resolution, and minimum-safe-correction guidance for the requirements its base half already states. It introduces no independent target — anything a draft has to meet is a base rule, and belongs in the base half where the writing Skill will actually see it — and it restates no base rule in other words, because a requirement and its diagnostic drift apart the moment both claim to say what is required.

Writing the review half is the work of the Skill that reviews, and its absence is not a defect: a base half with no extension beside it is a complete resource.

## Adding a genre or a technique

Write one file in the right directory, name it for the canonical value, and give it a base half. Add the review extension beside it if there is diagnostic guidance to carry. Then check that a Skill can reach it: the value is the filename, so anything that reads the directory finds it without an edit anywhere else.
