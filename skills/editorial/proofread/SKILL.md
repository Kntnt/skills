---
name: proofread
description: Correct only mechanical language errors — spelling, grammar, punctuation, agreement, inflection, duplicated or missing words, and locale mechanics — in one supplied text, preserving its wording, meaning, tone, structure, formatting, and metadata. Start it on your own only when a specific text is at hand and the request either uses a proofreading term (proofread, spell-check, copyedit, fix the typos, korrekturläs, rätta stavfelen) or is unambiguously limited to mechanical language errors. Not for a request to edit, rewrite, polish, improve, tighten, or review a text — each of those asks for changes this Skill refuses to make. A user may also invoke it by name at any time.
disable-model-invocation: false
argument-hint: '[--language=<selector>] [--output=<response|path>] [<text>|<path>|<url>] | [--language=<selector>] --in-place[=on|off] <path> [-- <instruction>]'
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# proofread

Correct the mechanical language errors in one supplied Text Artifact, and change nothing else about it.

**Dependencies.** Checker: `$HERE/../kntnt/scripts/kntnt.py` if that file exists, else `kntnt/scripts/kntnt.py` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Run `uv run "<checker>" check --here="$HERE"`. Exit 2: emit stdout and stop. If no checker is found, tell the user to install the Manager (`npx skills add Kntnt/skills`).

`$HERE` is the directory that contains this SKILL.md.

`$LIBRARY` is `library/` under the Manager directory that contains the checker. If it is absent, tell the user to run `/kntnt update`, then stop.

A model-invoked run changes only how the Skill starts. Once started, it takes the specific Text Artifact the current turn identifies as the omitted operand and enters the same numbered steps as invocation by name. The paths join before loading any language or editorial resource; the trigger wording is not a second source of rules or an alternate execution path.

## Invocation Envelope

Before help routing or formal validation, read the `## INVOCATION ENVELOPE` section of `$HERE/help.md` and follow it. Pass only the Formal Invocation to scripts and nested formal parsers. Apply Help and Arguments below only to the Formal Invocation.

## Help

If the arguments are `--help`, `-h`, or `help`, print `$HERE/help.md` verbatim and stop.

## Arguments

Two forms, each carrying exactly one Text Artifact:

- `/proofread [--language=<selector>] [--output=<response|path>] [<text>|<path>|<url>]`
- `/proofread [--language=<selector>] --in-place[=on|off] <path>`

The operand is the Text Artifact: inline text, one local path, or one URL. Where the invocation carries no operand, it is the single text the current turn identifies.

`--language=<selector>` names the language or locale whose mechanics apply. Any spelling the Collection's resolver reaches is accepted — a canonical code (`sv`, `en_GB`), a case or separator variant of one (`en-GB`, `EN_GB`), a curated alias (`BrE`, `brittisk engelska`), or an ordinary description of a language in any language.

`--output=<response|path>` names the Output Target. `response` is the default and the value `response` states it explicitly; anything else is one filesystem path.

`--in-place[=<value>]` selects In-place Editing. It accepts `yes`, `on`, and `true` against `no`, `off`, and `false`; bare `--in-place` means `on`, `--in-place=off` has the same effect as omitting the option, and the default is `off`.

Invalid forms, each refused the same way:

- A `--`-prefixed token that is not `--language`, `--output`, or `--in-place`.
- `--language` or `--output` without a value, or `--in-place` with a value outside the vocabulary above.
- `--output` and `--in-place=on` in one invocation, which name two destinations for one text.
- More than one Text Artifact — several paths, a glob reaching more than one file, or a directory of texts.
- An out-of-order form: the Text Artifact written before a flag rather than after every flag.

Name in one line what was wrong, print the `## SYNOPSIS` section of `$HERE/help.md` verbatim, and point at `/proofread --help` for the page in full. Then correct nothing, write nothing, and stop. A flag is refused rather than ignored where it has no work to do here, because a flag accepted and ignored teaches that flags sometimes do nothing.

## Steps

1. Parse the arguments by the rules above and settle the single Text Artifact. An invalid form takes the refusal those rules describe. Done when one Text Artifact and a valid set of options are in hand, or you have stopped.
2. Settle the destination before anything is corrected, following `$LIBRARY/references/delivery.md`. Make every refusal that contract names by reading alone — In-place Editing together with a separate Output Target, an output path equal to the input path, In-place Editing against inline text or a URL or a source that is not a writable local file, and a destination whose parent directory does not exist — so that a refusal has nothing written behind it. Done when the destination is settled, or you have stopped.
3. Read the Text Artifact's leading YAML frontmatter where it has any, and look in it for one top-level `kntnt` map. That map is the only Kntnt configuration a document carries; `language`, `lang`, `genre`, `technique`, and every other key outside it are the document's own fields, whatever they are named and whatever they hold. Read `language` out of the map and nothing else out of it. Done when the artifact's recognized language value is known to be present, absent, or unreachable.
4. Resolve the language, taking the first of these that answers: the `--language` value; the recognized `kntnt` map's `language` value from step 3; the current Contextual Instruction; applicable Conversation Context; then the language of the Text Artifact itself, which is what inference reads and what the default already is. Suppression is that precedence working rather than an error: a Contextual Instruction every higher level has already settled leaves nothing for it to settle, and the run continues rather than refusing it as unaddressable guidance. Where saying so is useful, the delivery names the suppressed instruction beside the resolved configuration. Where that language is materially ambiguous or mixed — no dominant language, or alternation inside paragraphs — ask which language to proofread in rather than choosing one. Nothing has been written yet, so asking costs nothing to undo. Done when exactly one selector is in hand, or you have asked.
5. If step 3 found a recognized `kntnt` map whose `language` value no installed resource answers to, and `--language` supplied no value, report it as unusable artifact metadata: name the value, say that it is neither a canonical code nor an installed alias, and stop. Do not read it as the code it resembles. A `--language` value settles the parameter and suppresses this, the unusable map then being none of the run's business. Done when the run has stopped, or the metadata is not in the way.
6. Run `uv run "$LIBRARY/scripts/languages.py" resolve --scope=mechanics "<selector>"`. Exit 0: take the reported `code` as the resolved language and the `mechanics` scope as this run's language-specific rules. A non-zero exit means the selector reached no single installed resource — interpret the human description semantically, propose one candidate from `uv run "$LIBRARY/scripts/languages.py" list`, and verify it through the same `resolve` command; ask only where no unique installed candidate can be established. Then load `$LIBRARY/references/editorial/mechanics.md`, the shared mechanics contract, which holds the rules of objective correctness that do not depend on the language; it and the resolved scope together are this run's rules, and the scope is the more specific of the two wherever they meet. That one document is the whole of what is admitted from the Collection's editorial resources: load no base contract, no genre, no technique, and no anti-slop catalogue, load no other scope, and read no composition, review, or anti-slop guidance from anywhere. Done when the contract and the mechanics scope are both in hand, or you have stopped.
7. Correct every objective mechanical error in the resolved language, reading the text yourself: misspellings, grammatical errors, punctuation errors, agreement between subject and verb or noun and modifier, wrong inflection, a duplicated word, a word plainly missing, and the locale's own conventions for dates, numbers, currency, and quotation as the mechanics scope states them, together with everything the shared mechanics contract holds. Correct all of them — a mechanical pass that leaves mechanical errors behind is a pass the user has to make again. A resolved locale establishes its date conventions but not what ambiguous source fields meant: `3/4` stays exactly `3/4` under both `en_GB` and `en_US` unless the Text Artifact itself establishes one reading; never expand or reorder it solely from locale. A grammatically valid word-as-word phrase such as `the word probably` remains unmarked: add no quotation marks or other emphasis unless the loaded rules identify an objective error. A code sample — a fenced block, an indented block, or an inline code span — is quoted material rather than the text's own prose: its contents are read past rather than read against the rules, so nothing inside one is a finding and nothing inside one is changed, the docstrings, comments, and string literals among them. Prose about code is ordinary prose and is read like every other sentence. Introduce no spellchecker, grammar service, or scanner of your own; the resolver above is the only script this Skill runs. Done when the mechanical errors you can identify are corrected.
8. Change nothing else. Wording, meaning, tone, register, argument, structure, factual content, formatting and markup, code and its contents, links, and metadata all come through untouched, and the frontmatter comes through byte for byte — a language value you were entitled to read is read and left exactly where it is, no `kntnt` map is added or removed, and nothing is reordered. A preference is not an error, and the rules step 6 put in hand are what says which is which: what neither of them names as an error comes through untouched, however tempting it is, and what either of them does name is corrected however deliberate it looks. A sentence improved here is the failure this Skill exists to prevent: mechanical correction was requested, and mechanical correction is the whole of what is delivered. Done when the diff you are about to deliver is mechanical throughout.
9. Deliver by `$LIBRARY/references/delivery.md`: the complete Text Artifact to the settled Output Target, the source file replaced where In-place Editing was requested, and a derived filename with its collisions resolved where the target is a directory. Where nothing was corrected and the destination is the response or the source file itself, write nothing at all and return only the short no-change status, in the language of the Text Artifact. Done when the Text Artifact has been delivered, or the no-change status has been reported.
