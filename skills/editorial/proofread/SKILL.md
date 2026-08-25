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

`$HERE` is the directory that contains this SKILL.md, and `$LIBRARY` is `library/` under the Manager directory that contains the checker — absent, tell the user to run `/kntnt update`, then stop.

## Invocation

Read `$LIBRARY/references/invocation-envelope.md` and follow it before help routing or formal validation; only the Formal Invocation reaches Help, Arguments, scripts, and nested formal parsers. `--help`, `-h`, and `help` print `$HERE/help.md` verbatim and stop.

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

Each is refused as `$LIBRARY/references/invocation-envelope.md` says; then correct nothing, write nothing, and stop.

## Steps

1. Parse the arguments by the rules above and settle the single Text Artifact. An invalid form takes the refusal those rules describe. Done when one Text Artifact and a valid set of options are in hand, or you have stopped.
2. Settle the destination before anything is corrected, following `$LIBRARY/references/delivery.md`. Make every refusal that contract names by reading alone — In-place Editing together with a separate Output Target, an output path equal to the input path, In-place Editing against inline text or a URL or a source that is not a writable local file, and a destination whose parent directory does not exist — so that a refusal has nothing written behind it. Done when the destination is settled, or you have stopped.
3. Read the Text Artifact's leading YAML frontmatter where it has any, and look in it for one top-level `kntnt` map. That map is the only Kntnt configuration a document carries; `language`, `lang`, `genre`, `technique`, and every other key outside it are the document's own fields, whatever they are named and whatever they hold. Read `language` out of the map and nothing else out of it. Done when the artifact's recognized language value is known to be present, absent, or unreachable.
4. Resolve the language, taking the first of these that answers: the `--language` value; the recognized `kntnt` map's `language` value from step 3; the current Contextual Instruction; applicable Conversation Context; then the language of the Text Artifact itself, which is what inference reads and what the default already is. Where that language is materially ambiguous or mixed — no dominant language, or alternation inside paragraphs — ask which language to proofread in rather than choosing one. Nothing has been written yet, so asking costs nothing to undo. Done when exactly one selector is in hand, or you have asked.
5. If step 3 found a recognized `kntnt` map whose `language` value no installed resource answers to, and `--language` supplied no value, report it as unusable artifact metadata: name the value, say that it is neither a canonical code nor an installed alias, and stop. Do not read it as the code it resembles. A `--language` value settles the parameter and suppresses this, the unusable map then being none of the run's business. Done when the run has stopped, or the metadata is not in the way.
6. Run `uv run "$LIBRARY/scripts/languages.py" resolve --scope=mechanics "<selector>"`. Exit 0: take the reported `code` as the resolved language and the `mechanics` scope as this run's language-specific rules. A non-zero exit means the selector reached no single installed resource — interpret the human description semantically, propose one candidate from `uv run "$LIBRARY/scripts/languages.py" list`, and verify it through the same `resolve` command; ask only where no unique installed candidate can be established. Load no other scope, and read no composition, review, or anti-slop guidance from anywhere. Done when the mechanics scope is in hand, or you have stopped.
7. Correct every objective mechanical error in the resolved language, reading the text yourself: misspellings, grammatical errors, punctuation errors, agreement between subject and verb or noun and modifier, wrong inflection, a duplicated word, a word plainly missing, and the locale's own conventions for dates, numbers, currency, and quotation as the mechanics scope states them. Correct all of them — a mechanical pass that leaves mechanical errors behind is a pass the user has to make again. Introduce no spellchecker, grammar service, or scanner of your own; the resolver above is the only script this Skill runs. Done when the mechanical errors you can identify are corrected.
8. Change nothing else. Wording, meaning, tone, register, argument, structure, factual content, formatting and markup, code and its contents, links, and metadata all come through untouched, and the frontmatter comes through byte for byte — a language value you were entitled to read is read and left exactly where it is, no `kntnt` map is added or removed, and nothing is reordered. Where more than one form is correct — two established spellings, a serial comma present or absent, a variant the mechanics scope names as valid — the text's own choice stands, because a preference is not an error. A sentence improved here is the failure this Skill exists to prevent: mechanical correction was requested, and mechanical correction is the whole of what is delivered. Done when the diff you are about to deliver is mechanical throughout.
9. Deliver by `$LIBRARY/references/delivery.md`: the complete Text Artifact to the settled Output Target, the source file replaced where In-place Editing was requested, and a derived filename with its collisions resolved where the target is a directory. Where nothing was corrected and the destination is the response or the source file itself, write nothing at all and return only the short no-change status, in the language of the Text Artifact. Done when the Text Artifact has been delivered, or the no-change status has been reported.
