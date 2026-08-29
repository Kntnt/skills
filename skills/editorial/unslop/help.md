# unslop

## NAME

unslop - apply the anti-slop pass alone to one text and change nothing else

## SYNOPSIS

**/unslop** [**--language**=*LANGUAGE*] [**--max**=*N*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/unslop** [**--language**=*LANGUAGE*] [**--max**=*N*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`unslop` applies the anti-slop catalogue to one otherwise finished text, corrects findings within the Correction Budget, reports anything left, and stops.

The catalogue covers seven semantic patterns: false contrast, empty opening, importance inflation, vague attribution, synonym cycling, robotic rhythm, and generic conclusion. They are recognized by function in the target language, not by matching English phrases.

Nothing outside that lens is corrected. The Skill applies no base editorial contract, genre, technique, wider language guidance, or fact check. Use `redline` for the full editorial contract.

A code sample is quoted material. Fenced blocks, indented blocks, and inline code are neither reviewed nor changed; prose about code is ordinary prose.

The Skill does not correct spelling, grammar, or punctuation. Locale conventions for spelling, vocabulary, dates, and currency never become findings. Use `proofread` for mechanical correction.

No provenance is required. Language resolves from **--language**, then a `language` value in a leading `kntnt` frontmatter map, the Contextual Instruction, Conversation Context, and finally the text. Mixed or ambiguous language produces a question.

A Contextual Instruction every higher level has already settled is suppressed rather than refused: the run continues, and the delivery names the suppressed instruction beside the resolved configuration where saying so is useful.

Ordinary frontmatter is not configuration. No `kntnt` map is created or updated. Unsupported `kntnt` language metadata stops the run unless **--language** overrides it.

Source material is outside the contract. The pass judges only the supplied text.

The Correction Budget is any non-negative integer and defaults to one. `0` reports findings without correction; a larger value is a ceiling, not a quota.

Each correction uses a fresh subagent with the complete current text and findings. Returned text is compared with the pre-round text and reviewed again before acceptance.

A correction removes the pattern without removing the passage's claim. A claim-losing correction is rejected and restored, and every removed claim is reported.

The loop stops when the text is clean, the budget is spent, a correction makes no relevant progress, or re-review raises a finding an earlier round's own repair created. Remaining findings are marked unresolved.

Repairs are the smallest changes that remove a pattern while preserving the writer's vocabulary, tone, uncertainty, and deliberate rhythm.

One invocation handles exactly one text. Multiple files, globs, and directories are refused.

The response is the default Output Target. **--output** writes elsewhere; **--in-place** replaces one writable local source file. The Skill reports the findings separately, in the text's own language, and every removed claim remains visible. Internal review reasoning is not output.

A model never starts this Skill on its own. Typing `/unslop` is the complete trigger.

## POSITIONAL ARGUMENTS

*TEXT*|*PATH*|*URL*

The single text to read, supplied inline, as a local path, or as a URL. When omitted, the current turn must identify it. In-place editing requires *PATH*. A brief, outline, or request supplied as the operand is reviewed like any other text; it is not carried out.

## OPTIONS

**--language**=*LANGUAGE*

Select the language or locale by canonical code, case or separator variant, curated alias, or ordinary description. It overrides every other source.

**--max**=*N*

Set the maximum number of corrections. It accepts any non-negative integer and defaults to `1`. `0` only reads and reports.

**--output**=*TARGET*

Deliver to `response` (the default) or one filesystem path. A new path creates a file, an existing file is replaced, and an existing directory receives a derived non-colliding filename. It cannot be combined with **--in-place** or name the source path.

**--in-place**[=**on**|**off**]

Replace the writable local source file. Bare **--in-place** means `on`; accepted values are `yes`, `on`, `true`, `no`, `off`, and `false`. Inline text, URLs, uploaded or read-only sources, and simultaneous **--output** are refused.

## DIAGNOSTICS

An invalid form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/unslop --help`. A flag is refused rather than ignored where it has no work to do here.

Refusals include unknown, missing, repeated, or out-of-order input; unsupported language; invalid budgets; multiple texts; incompatible output options; unsafe in-place sources; and unwritable destinations.

Unsupported `kntnt` language metadata stops the run unless **--language** overrides it. Mixed or ambiguous language produces one question before anything is written.

## EXAMPLES

**/unslop article.md**

Review `article.md`, allow one correction, and return the result without changing the file or correcting mechanics.

**/unslop --max=0 article.md**

Report findings without correcting them.

**/unslop --language=sv --max=3 --in-place utkast.md**

Allow up to three Swedish corrections and replace `utkast.md`.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

The following schematic cases pin the split independently of any one Skill's Formal Invocation grammar; `\n\n` denotes two newline characters in one payload.

| Case | Envelope | Formal Invocation | Contextual Instruction | Outcome |
| --- | --- | --- | --- | --- |
| Same line | `/skill --force -- Preserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Blank lines | `/skill --force --\n\nPreserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Empty suffix | `/skill --force --   ` | `/skill --force` | — | Syntax refusal |
| Later separator | `/skill -- Preserve -- deployment facts` | `/skill` | `Preserve -- deployment facts` | Envelope valid; formal grammar next |
| No separator | `/skill Preserve deployment facts` | `/skill Preserve deployment facts` | — | No split; formal grammar decides |
| Attached and quoted | ``/skill --force foo--bar `--` "--"`` | ``/skill --force foo--bar `--` "--"`` | — | No split; formal grammar decides |
| Exact help | `/skill --help -- Explain this page` | `/skill --help` | `Explain this page` | Context refusal; render nothing |

## DEPENDENCIES

`uv`; the Kntnt Manager, whose Collection Library carries the anti-slop catalogue and the language resources this Skill resolves against; and a harness that can run subagents, which stays a requirement whatever Correction Budget an invocation names. No other Skill.

## SEE ALSO

**/redline**, **/proofread**, **/write**, **/kntnt select**
