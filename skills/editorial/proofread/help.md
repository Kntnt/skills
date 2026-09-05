# proofread

## NAME

proofread - correct a text's mechanical language errors and nothing else

## SYNOPSIS

**/proofread** [**--language**=*LANGUAGE*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/proofread** [**--language**=*LANGUAGE*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`proofread` corrects spelling, grammar, punctuation, agreement, inflection, duplicated or missing words, and locale conventions for dates, numbers, currency, and quotation in one text.

It preserves wording, meaning, tone, structure, facts, formatting, code, links, metadata, and frontmatter. When several forms are correct, the text's existing choice stands. It never rewrites for style.

A code sample is quoted material. Fenced blocks, indented blocks, and inline code are neither checked nor changed; prose about code is treated as ordinary prose.

The text may come from any source, but one invocation handles exactly one text. Multiple files, globs, and directories are refused.

Language resolves from **--language**, then a `language` value in a leading `kntnt` frontmatter map, the Contextual Instruction, Conversation Context, and finally the text. Mixed or ambiguous language produces a question.

A Contextual Instruction every higher level has already settled is suppressed rather than refused: the run continues, and the delivery names the suppressed instruction beside the resolved configuration where saying so is useful.

Only the resolved language's mechanics guidance and the shared mechanics contract are used. Ordinary frontmatter is not configuration, and an unsupported `kntnt` language stops the run unless **--language** overrides it.

The default Output Target is the response. **--output** writes elsewhere; **--in-place** replaces the single writable local source file. An unchanged result is not rewritten unless delivery to another path was requested.

A model may start this Skill only for a specific text and an explicit proofreading request. Requests to edit, rewrite, polish, improve, tighten, or review do not trigger it; typing `/proofread` always does.

Where no Formal Invocation carries an Output Target, the current turn must settle it. An unnamed destination resolves to the response, and a file named only as the location of the errors names no destination. `Fix the spelling and grammar mistakes in case.md` delivers to the response.

An explicit separate destination selects that Output Target: `Write the corrected text to corrected.md` selects corrected.md as a separate Output Target. A request that asks for the file itself to be changed selects In-place Editing: `Update case.md with the grammar corrections` selects In-place Editing.

In-place Editing remains subject to every refusal, including inline text, a URL, a read-only source, more than one text, or a simultaneous separate Output Target.

A request that only says to save or apply the result is materially ambiguous about the destination: `Fix the grammar errors in case.md and save the corrections` asks which destination the caller intends. In every such case, ask which destination the caller intends and write nothing.

## POSITIONAL ARGUMENTS

*TEXT*|*PATH*|*URL*

The single text to proofread, supplied inline, as a local path, or as a URL. When omitted, the current turn must identify it. In-place editing requires *PATH*.

## OPTIONS

**--language**=*LANGUAGE*

Select the language or locale whose mechanics apply. Canonical codes, case or separator variants, curated aliases, and ordinary language descriptions are accepted. The option overrides every other source.

**--output**=*TARGET*

Deliver to `response` (the default) or one filesystem path. A new path creates a file, an existing file is replaced, and an existing directory receives a derived non-colliding filename. It cannot be combined with **--in-place** or name the source path.

**--in-place**[=**on**|**off**]

Replace the writable local source file. Bare **--in-place** means `on`; accepted values are `yes`, `on`, `true`, `no`, `off`, and `false`. Inline text, URLs, uploaded or read-only sources, and simultaneous **--output** are refused.

## DIAGNOSTICS

An invalid form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/proofread --help`. A flag is refused rather than ignored where it has no work to do here.

Refusals include undeclared or out-of-order input, invalid option values, multiple texts, incompatible output options, unsafe in-place sources, and destinations whose parent does not exist.

Unsupported `kntnt` language metadata stops the run unless **--language** overrides it. Mixed or ambiguous language produces one question before anything is written.

## EXAMPLES

**/proofread report.md**

Correct `report.md` and return the result in the response without changing the file.

**/proofread --in-place report.md**

Correct and replace `report.md`. An unchanged file is not rewritten.

**/proofread --language=en_GB --output=~/texts notes.md**

Use British English mechanics and deliver a non-colliding file under `~/texts`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv`, and the Kntnt Manager, whose Collection Library carries the language resources this Skill resolves against. No other Skill.

## SEE ALSO

**/kntnt select**
