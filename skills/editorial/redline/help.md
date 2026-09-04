# redline

## NAME

redline - review one text against the editorial contract, correct what it finds, and close with one mechanical pass

## SYNOPSIS

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--max**=*N*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--max**=*N*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`redline` reviews one text against the base editorial contract, resolved genre, optional technique, anti-slop catalogue, and resolved language guidance. It corrects findings within the Correction Budget, reports anything left, and ends with one mechanical pass.

No provenance is required. A leading `kntnt` frontmatter map supplies defaults and is updated to match the run; no map is created when none exists. A `technique: none` in that map is its value for no technique rather than a missing one, so a text written without one is reviewed without one.

Genre, technique, and language resolve independently from the Formal Invocation, `kntnt` metadata, the Contextual Instruction, Conversation Context, inference, the resolved genre's ordinary technique, and defaults. Defaults are `general`, no technique, and the text's language. The delivery says which technique was resolved and where it came from. A technique is never inferred, and mixed language produces a question.

A Contextual Instruction every higher level has already settled is suppressed rather than refused: the run continues, and the delivery names the suppressed instruction beside the resolved configuration where saying so is useful.

Ordinary frontmatter is not configuration. Unsupported `kntnt` values stop the run unless the corresponding flag overrides them.

Source material is outside the contract. The review judges only the supplied text; visible contradictions or unsupported claims may still be findings.

A code sample is quoted material. Fenced blocks, indented blocks, and inline code are neither reviewed nor changed; prose about code is ordinary prose.

The final `proofread` pass runs exactly once with the resolved language. No substantive edit follows it, and only mechanically relevant guidance is forwarded.

The Correction Budget is any non-negative integer and defaults to one. `0` reports findings without substantive correction but still runs the final mechanical pass. A larger value is a ceiling, not a quota.

Each correction uses a fresh subagent with the complete current text and current findings. Returned text is compared with the pre-round text and reviewed again before acceptance.

A correction must repair the finding without removing the passage's claim. A claim-losing correction is rejected and restored, and every removed claim is reported.

The loop stops when the text is clean, the budget is spent, a correction makes no relevant progress, or re-review raises a finding an earlier round's own repair created. Remaining findings are marked unresolved.

One invocation handles exactly one text. Multiple files, globs, and directories are refused.

The response is the default Output Target. **--output** writes elsewhere; **--in-place** replaces one writable local source file. The Skill reports the findings separately, in the text's own language, and every removed claim remains visible. Internal review reasoning is not output.

## POSITIONAL ARGUMENTS

*TEXT*|*PATH*|*URL*

The single text to review, supplied inline, as a local path, or as a URL. When omitted, the current turn must identify it. In-place editing requires *PATH*.

## OPTIONS

**--genre**=*GENRE*

Select an installed genre. The default is `general`; an unknown genre is refused.

**--technique**=*TECHNIQUE*

Select an installed structural technique. Where none is named here, in the text's `kntnt` map, in an instruction, or in applicable conversation context, the resolved genre's ordinary technique applies. To review against no technique, say so in an instruction or carry `technique: none` in the map: this flag takes an installed name and cannot say none. Resemblance never selects one.

**--language**=*LANGUAGE*

Select the language or locale by canonical code, case or separator variant, curated alias, or ordinary description. It overrides every other source and is passed to `proofread`.

**--max**=*N*

Set the maximum number of substantive corrections. It accepts any non-negative integer and defaults to `1`. `0` only reviews and reports; the final mechanical pass still runs.

**--output**=*TARGET*

Deliver to `response` (the default) or one filesystem path. A new path creates a file, an existing file is replaced, and an existing directory receives a derived non-colliding filename. It cannot be combined with **--in-place** or name the source path.

**--in-place**[=**on**|**off**]

Replace the writable local source file. Bare **--in-place** means `on`; accepted values are `yes`, `on`, `true`, `no`, `off`, and `false`. Inline text, URLs, uploaded or read-only sources, and simultaneous **--output** are refused.

## DIAGNOSTICS

An invalid form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/redline --help`. A flag is refused rather than ignored where it has no work to do here.

Refusals include unknown, missing, repeated, or out-of-order input; unsupported resources; invalid budgets; multiple texts; incompatible output options; unsafe in-place sources; and unwritable destinations. This is the whole of what is refused over the form of an invocation.

Other stops are documented with the value they concern and under `## INVOCATION ENVELOPE`.

A valid text is reviewed even when it is a brief, outline, or notes. Its incompleteness becomes a finding, not a refusal.

Unsupported `kntnt` metadata stops the run unless a flag overrides it. Mixed or ambiguous language produces one question before anything is written.

## EXAMPLES

**/redline article.md**

Review `article.md`, allow one correction, proofread the result, and return it without changing the file.

**/redline --max=0 article.md**

Report editorial findings without correcting them; the final mechanical pass still runs.

**/redline --genre=press-release --language=sv --in-place utkast.md**

Review and replace `utkast.md` as a Swedish press release.

**/redline --technique=abt --output=~/reviewed draft.md**

Apply the ABT technique and deliver a non-colliding file under `~/reviewed`.

**/redline --genre=report --max=0 handoff.md -- Review it as a PAC piece in Swedish.**

Review `handoff.md` as a report without substantive correction. If its `kntnt` map already settles technique and language, the Contextual Instruction is suppressed and the review still runs.

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

`uv`; the Kntnt Manager, whose Collection Library carries the editorial contract, the genres and techniques, the anti-slop catalogue, and the language resources this Skill resolves against; the `proofread` Skill, which performs the closing mechanical pass; and a harness that can run subagents, which stays a requirement whatever Correction Budget an invocation names.

## SEE ALSO

**/write**, **/proofread**, **/kntnt select**
