# proofread

## NAME

proofread - correct a text's mechanical language errors and nothing else

## SYNOPSIS

**/proofread** [**--language**=*LANGUAGE*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/proofread** [**--language**=*LANGUAGE*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`proofread` takes one text and removes its mechanical language errors. It corrects spelling, grammar, punctuation, agreement between subject and verb or noun and modifier, inflection, duplicated and missing words, and the locale's own conventions for dates, numbers, currency, and quotation.

Everything else is preserved. Wording, meaning, tone, register, argument, structure, factual content, formatting and markup, code, links, and metadata come through untouched, and frontmatter comes through byte for byte. Where more than one form is correct — two established spellings, a serial comma present or absent, a variant the language's own mechanics name as valid — the text's own choice stands, because a preference is not an error. Asking for mechanical correction never returns a rewrite, however much better the rewrite might have read.

The Skill needs no other Skill and no provenance. A text written by hand, produced elsewhere, or pasted out of another tool is proofread exactly as one this collection wrote.

One invocation processes one text. Several paths, a glob reaching more than one file, or a directory of texts is refused rather than resolved into a configuration per file, because the language, the destination, and any replacement of a source are settled once and for one text.

The language is resolved by a fixed precedence, and the first of these that answers wins: the **--language** value, a `language` value in a `kntnt` map in the text's own leading frontmatter, the Contextual Instruction, applicable Conversation Context, and then the language of the text itself, which is also the default. A text whose language is materially ambiguous or mixed — no dominant language, or alternation inside paragraphs — is asked about rather than guessed at. Only that language's mechanics are loaded; no composition, review, or anti-slop guidance is read.

Ordinary document frontmatter is never configuration. A `language`, `lang`, `genre`, or `technique` key sitting at the top level of a document's own frontmatter belongs to that document, and only a `kntnt` map is read as this collection's. Where such a map carries a language no installed resource answers to, and no **--language** value supersedes it, the run reports unusable artifact metadata and stops rather than reading it as the code it resembles.

Delivery changes nothing on disk unless it is asked to. The default target is the response; **--output** names a file or an existing directory, and **--in-place** replaces the single writable local file the text came from. A run that finds nothing to correct and was aimed at the response or at its own source writes nothing and returns a short no-change status in the text's own language; a run aimed at a different file or directory delivers the complete text whether or not anything changed.

A model may start this Skill on its own, but only for a specific text and only where the request either uses a proofreading term or is unambiguously limited to mechanical language errors. A request to edit, rewrite, polish, improve, tighten, or review a text is not such a request and does not start it. Typing `/proofread` starts it at any time, which is how the conservative contract stays directly reachable.

## POSITIONAL ARGUMENTS

*TEXT*|*PATH*|*URL*

The text to proofread, supplied inline, as one local path, or as one URL. Omitted, it is the single text the current turn identifies. In-place editing requires the *PATH* form.

## OPTIONS

**--language**=*LANGUAGE*

The language or locale whose mechanics apply. It accepts a canonical code (`sv`, `en_GB`), a case or separator variant of one (`en-GB`, `EN_GB`), a curated alias (`BrE`, `brittisk engelska`), or an ordinary description of a language written in any language. It overrides every other source, including a `kntnt` map in the text's frontmatter. Without it the precedence in DESCRIPTION applies, ending at the language of the text itself.

**--output**=*TARGET*

Where the resulting text is delivered. `response` is the default and states that default explicitly; any other value is one filesystem path. A path that does not exist creates exactly that file, a path naming an existing file replaces it without asking for a second confirmation, and a path naming an existing directory receives a filename derived from the source, never overwriting what is already there. It cannot be combined with **--in-place**, and naming the source's own path is refused in favour of **--in-place**.

**--in-place**[=**on**|**off**]

Replace the file the text came from with the result. It accepts `yes`, `on`, and `true` against `no`, `off`, and `false`; bare **--in-place** means `on`, and `off` is both the default and the value that has the same effect as omitting the option. It requires exactly one writable local file and is refused for inline text, a URL, an uploaded or read-only source, and for any invocation that also names an output.

## DIAGNOSTICS

An incomplete or invalid form is refused rather than repaired or ignored. The Skill names in one line what was wrong, prints the SYNOPSIS, corrects nothing, writes nothing, and points at `/proofread --help`. A flag with no work to do is refused rather than ignored, an accepted and ignored flag teaching that flags sometimes do nothing.

Refused before any side effect, so that nothing is left half done: an undeclared flag, a text written before a flag rather than after every flag, a missing or invalid option value, more than one text in one invocation, **--output** together with **--in-place**, an output path equal to the input path, in-place editing of inline text, a URL, or a read-only or non-local source, and a destination whose parent directory does not exist.

A `kntnt` map naming a language that is neither a canonical code nor an installed alias, where no **--language** value supersedes it, is reported as unusable artifact metadata. The run stops rather than reinterpreting the value, so a spelling such as `en_UK` never quietly becomes `en_GB`.

A text whose language cannot be settled — mixed, or a description matching no installed resource uniquely — produces one question rather than a guess. Nothing has been written at that point, so the question costs nothing to answer either way.

## EXAMPLES

**/proofread report.md**

Correct the mechanical errors in `report.md`, infer the language from the file, and return the corrected text in the response. `report.md` itself is left alone.

**/proofread --in-place report.md**

Correct the same file and replace it with the result. If nothing needed correcting, the file is not rewritten and a short status says so.

**/proofread --language=en_GB --output=~/texts notes.md**

Correct `notes.md` under British English mechanics and deliver it into the existing directory `~/texts`, under a filename derived from the source and never over an existing file.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv`, and the Kntnt Manager, whose Collection Library carries the language resources this Skill resolves against. No other Skill.

## SEE ALSO

**/kntnt select**
