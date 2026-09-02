---
name: write
description: Turn a brief and its source material into one truthful first draft in the target language, and stop there. Start it on your own only when the literal token `/write` appears in the request or in an instruction the request points at — inside a longer message, a document, or a checklist that says to run it. Not for a bare request to write, draft, compose, summarise, rewrite, edit, or review something — without `/write` in it, such a request is answered as it otherwise would be. A user may also invoke it by name at any time.
disable-model-invocation: false
argument-hint: '[--genre=<genre>] [--technique=<technique>] [--language=<language>] [--frontmatter=<yes|no>] [--output=<response|path>] [<brief>] [-- <instruction>]'
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# write

Turn a brief and whatever material it points at into one first draft, and stop. No review pass, no proofreading pass, no peer Skill: running an editorial pipeline is a separate choice the user makes afterwards.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run --no-cache --no-project "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

Run every UV command in this Skill with a fresh private directory as `TMPDIR`, and remove that directory after the command, including when it fails. The private directory belongs to that one command and no other run, so cleanup removes only files this run created.

`$HERE` is the directory that contains this SKILL.md.

`$LIBRARY` is `library/` under the Manager directory that contains the checker. If it is absent, tell the user to run `/kntnt update`, then stop.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

`/write [--genre=<genre>] [--technique=<technique>] [--language=<language>] [--frontmatter=<yes|no>] [--output=<response|path>] [<brief>]`, and nothing else.

- `<brief>` is free text in any language. It may state what to write and it may point at material — a local path, a URL, a passage pasted in whole.
- `--genre=<genre>` names a resource under `$LIBRARY/references/editorial/genres/`, by its filename without the extension.
- `--technique=<technique>` names a resource under `$LIBRARY/references/editorial/techniques/`, the same way.
- `--language=<language>` is any selector `$LIBRARY/scripts/languages.py` accepts: a canonical code, a curated alias, or a description of a language in words.
- `--frontmatter=<yes|no>` accepts `yes`, `on`, or `true` and `no`, `off`, or `false`.
- `--output=<response|path>` accepts the keyword `response` or one filesystem path.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not one of the five options, or one of them written without `=` and a value.
- The same option given twice, or given an empty value.
- `--frontmatter` with a value outside the two vocabularies above.
- `--genre` or `--technique` naming a resource that is not installed.
- `--language` reaching no installed Language Resource, or more than one.
- `--output` naming a path whose parent directory does not exist, or naming a local file that supplied material for this run.
- Nothing to write: no brief, no material, and no applicable guidance in context.
- An out-of-order form: the brief written before an option rather than after every option.

Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/write --help` for the page in full. Then write nothing, deliver nothing, and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Resolution

Genre, technique, language, and the two output options are each resolved on their own, in this order of precedence:

1. The Formal Invocation.
2. A recognized Kntnt map in the leading YAML frontmatter of supplied material — the reserved `kntnt` key and its `genre`, `technique`, and `language` values, and nothing else. Frontmatter carrying no such map carries no configuration, whatever its other keys are called. The map never carries the output options, so this step is empty for them.
3. The current Contextual Instruction.
4. Applicable Conversation Context.
5. Inference from what was requested and what the material is.
6. The parameter's default: `general` for genre, no technique, the language of the request and the supplied material, the response for the Output Target, and on for the Kntnt map.

A value found at one level suppresses the levels below it for that parameter alone. An explicit genre and a language taken from context are an ordinary invocation, not a conflict. Suppression is that precedence working rather than an error: a Contextual Instruction every higher level has already settled leaves nothing for it to settle, and the run continues rather than refusing it as unaddressable guidance. Where saying so is useful, the delivery names the suppressed instruction beside the resolved configuration.

Two things are never inferred. A technique applies because it was selected — by the invocation, the map, or an instruction that names one — and never because the material or the draft happens to fall into its shape. A language is settled rather than guessed: where the request and the material are materially ambiguous or mixed, say what the candidates are and ask, before anything is written.

A genre inferred rather than named is inferred against what is installed. The genre directory is the list of installed values, and a run inferring one may read a single thing besides that listing: the opening of each installed genre resource — its `# <Name>` heading and the paragraph under it, which every resource carries so that a reader choosing between them has something to read without loading the rest. Read that far and no further. What a genre asks for is not evidence about whether that genre applies, so a resource read past its opening has been loaded rather than considered — and the loading step below is unchanged by any of this: it loads the genre inference settled on, and no other. Where no installed genre fits what is in front of you better than the default does, the default at the foot of the precedence stands.

A recognized Kntnt map whose value cannot be used — a language nothing installs, a genre or technique that is not there — is reported as unusable artifact metadata and stops the run, unless the Formal Invocation already settled that parameter. It is never quietly read as the nearest usable value.

## Steps

1. Parse the arguments by the rules above. An invalid form takes the refusal named there. Done when the form is settled, or you have stopped.
2. Gather the material: text inline in the brief, local files and URLs it points at, applicable Contextual Instruction, and applicable Conversation Context. Several sources feed one draft, and reading a file selects no destination. Done when everything the draft is answerable to is in hand, or you have refused for want of anything to write.
3. Resolve genre, technique, language, and the output options by `## Resolution`. A genre or technique is verified against the resources actually installed in the two directories named above. Where the genre has to be inferred rather than verified, `## Resolution` says what may be read to infer it. A language selector is verified by `uv run --no-cache --no-project "$LIBRARY/scripts/languages.py" resolve --scope=composition "<selector>"`, whose non-zero exit says which of the ways it failed and takes the refusal in `## Arguments`; an unlisted description of a language is interpreted first, then proposed as one installed candidate and verified through that same command. Where the language of the request and the material is materially ambiguous or mixed, name the candidates and ask before anything is written. Done when all five are settled, or you have asked or refused.
4. Settle the Output Target against `$LIBRARY/references/delivery.md`, and refuse a contradictory or unwritable destination before anything is written. In-place Editing is not offered here: this Skill creates a text and never replaces the material its brief came from, so an output path equal to a supplied file is refused rather than honoured. Done when the destination is known, or you have refused.
5. Load the contract, and nothing besides it: `$LIBRARY/references/editorial/base.md`, the selected genre from `$LIBRARY/references/editorial/genres/`, the resolved technique from `$LIBRARY/references/editorial/techniques/` where one was selected, and the composition scope the resolver already returned in step 3. A resource's review half — the file named for it with `.review.md` — belongs to the Skills that review, and so do the language's other scopes; none of them is loaded here. Done when those four are loaded and nothing else has been.
6. Write one draft that satisfies that contract. Source Fidelity is the invariant over all of it: invent no fact, and preserve attribution, uncertainty, scope, chronology, and causality exactly as the material has them. Where the material is speech to be quoted, read [`quotations.md`](references/quotations.md) first. Done when the draft is complete.
7. Unless the frontmatter option is off, attach the Handoff Metadata: a `kntnt` map in leading YAML frontmatter carrying the normalized `genre`, `technique`, and `language` and nothing else, with `none` where no technique was resolved. Merge it into the frontmatter the requested artifact already needs rather than writing a second block. Never embed the argument, the material, or the options this run was given. Turning it off removes that map alone and never the frontmatter the artifact itself requires. Done when the artifact carries what it should and nothing more.
8. Deliver by `$LIBRARY/references/delivery.md`, then stop. On a response target, remove every artifact or scratch file this run created and base the delivery account on the filesystem state that remains after cleanup. Say what was resolved, where the draft went, and where the material stopped: what the brief asked for that the material did not carry, and, where the draft is short of a stated length, what further material would close the gap. The account is answerable to the same contract as the draft, so it asserts no fidelity it has not established: a run reporting its own draft as faithful has made a claim about the draft like any other. Reviewing the draft and proofreading it are separate invocations the user makes afterwards; perform neither, and offer neither as a next step of this run. Done when the draft has been delivered.
