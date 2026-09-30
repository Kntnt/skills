# redline

## NAME

redline - review one text against the editorial contract and an optional Writing Brief, correct what it finds, and close with one mechanical pass

## SYNOPSIS

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--brief=**_PATH|URL_] [**--max**=*N*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--brief=**_PATH|URL_] [**--max**=*N*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`redline` reviews one text against the base editorial contract, resolved genre, optional technique, anti-slop catalogue, and resolved language guidance. For the five web genres it also reads their shared craft brief and its review guidance, for article, casestudy, column and opinion the article anatomy and the headline guidance, and for a press release the headline guidance, each with its review guidance. It corrects findings within the Correction Budget, reports anything left, and ends with one mechanical pass.

For those four genres the anatomy's counted limits are measured by a script at every review, so every count a finding reports is a measured one, and each correction agent measures its own repair before returning it. The measurement also exposes complete heading/following-text pairs and unjudged shared words. Both reviewer and correction agent judge semantic repetition from those pairs and the full text: necessary repeated names or topic words alone are no defect, and paraphrases can repeat with little overlap. Correction agents repair echoes named by findings or introduced by their own changes; unrelated pre-existing echoes are preserved and reported. A text the script cannot read is inspected by hand and said to be.

A press release's two counted limits, its headline's characters and its summary's words, are measured by the same script at every review and by each correction agent, so every count a finding reports about them is a measured one. For a press release the script reports no heading pairs: the reviewer reads the headline and the summary against each other.

An explicitly selected Writing Brief adds a **Brief fulfilment** section, even when the text is unchanged. The brief resolves from **--brief**, then a Contextual Instruction naming it for this review, then applicable Conversation Context naming it. Each level suppresses those below it; the delivery names a different brief suppressed by the option. A brief merely present from an earlier session turn is not selected. Without a selected brief, the ordinary review is unchanged.

The review maps a brief of any shape or language onto the Library's English 13-question template. Each answered question receives a fulfilled, partly fulfilled or not fulfilled status, evidence from the delivered text or explicit absence, and reader loss for a shortfall. Unanswered questions are named. A **[MISSING: …]**-only answer is unanswered; **[SUGGESTED: …]** and **[WEAK: …]** answers are assessed as written and flagged unconfirmed or weak. The brief itself is never reviewed, edited, proofread or delivered.

No provenance is required. A leading `kntnt` frontmatter map in the text supplies defaults and is updated to match the run; no map is created when none exists. A `technique: none` in that map is its value for no technique rather than a missing one, so a text written without one is reviewed without one.

Genre, technique, and language resolve independently from the Formal Invocation, the brief's `kntnt` metadata, the text's metadata for values the brief omits, the Contextual Instruction, Conversation Context, inference, the resolved genre's ordinary technique, and defaults. Defaults are `general`, no technique, and the text's language. Article, casestudy, column, opinion and webcopy ordinarily select no technique. Explicit selections and existing metadata keep their priority. The delivery says which technique was resolved and where it came from. A technique is never inferred, and mixed language produces a question.

A Contextual Instruction every higher level has already settled is suppressed rather than refused: the run continues, and the delivery names the suppressed instruction beside the resolved configuration where saying so is useful.

Disagreement between the two maps is always reported as a finding, even when an explicit option overrides both. The brief's map wins below the Formal Invocation and is never updated. With only one map, that map supplies defaults. Ordinary frontmatter is not configuration. Unsupported winning `kntnt` values stop the run unless the corresponding flag overrides them. A text-map value suppressed by the brief map is reported in the conflict.

Without a selected brief, source material is outside the contract. The review judges only the supplied text; visible contradictions or unsupported claims may still be findings. With a brief, the review reads the material it points at as needed for its requirements. Repairable shortfalls join the existing findings and Correction Budget. Source Fidelity binds these corrections: no fact, source or quotation may be added without support in the text or that material, with attribution, uncertainty, scope, chronology and causality intact. Shortfalls needing unavailable evidence are reported and left for the writer; a brief requirement is not itself evidence.

A code sample is quoted material. Fenced blocks, indented blocks, and inline code are neither reviewed nor changed; prose about code is ordinary prose.

The final `proofread` pass runs exactly once with the resolved language. A nested invocation refused before Proofread starts is corrected under the shared caller-recovery rule and consumes no pass or Correction Budget; a possible partial pass is established before anything resumes and is never blindly replayed. The complete result is required for delivery; an incomplete pass is reported as an obstacle. No substantive edit follows it, and only mechanically relevant guidance is forwarded.

The Correction Budget is any non-negative integer and defaults to one. `0` reports findings without substantive correction but still runs the final mechanical pass. A larger value is a ceiling, not a quota.

Each correction uses a fresh subagent with the complete current text and current findings. Returned text is a correction candidate: it is compared with the pre-round text and reviewed again before acceptance. Every difference in it traces to a finding of the review that commissioned the round, or to what repairing one required; a difference that traces to neither is restored from the pre-round text byte for byte, the rest of the round stands, and the restoration costs no budget and raises no finding.

A correction must repair the finding without removing the passage's claim. A claim-losing correction is rejected and restored, and every removed claim is reported, as is every changed claim — one left standing with its scope, certainty, attribution, chronology, causality or meaning moved — and every added claim, one the delivered text asserts and the text as it arrived has no counterpart for, an inference drawn from what that text already said among them. A sentence whose work is to bound what the text asserts is removed or weakened only on a finding naming a defect inside it, and only where a retained sentence still states the limit in full or the limit contradicts another passage.

The loop stops when the text is clean, the budget is spent, a correction makes no relevant progress, or re-review establishes a finding an earlier round's own repair created. A round established to have introduced a defect is rejected entire: the Text Artifact as it stood before that round is restored verbatim and is what the run delivers, the round keeps the budget it spent with no refund and no second attempt, and the attempt is reported apart from the findings the restored text still carries. A defect a round created is never reported as an unresolved finding for the caller to settle: the round is undone instead. Remaining findings are marked unresolved.

One invocation handles exactly one text. Multiple files, globs, and directories are refused.

The response is the default Output Target. A text delivered in the response arrives inside one fenced code block. **--output** writes elsewhere; **--in-place** replaces one writable local source file. The Skill reports the findings separately, in the text's own language, and every removed claim, every changed claim and every added claim remains visible. A changed headline, standfirst or subheading is reported with the defect that licensed the change, a changed claim by what it now asserts rather than how far its wording moved, and a removal that took a limit, a connective or a bounding clause by what the reader no longer has. The claim account is of the text delivered, the claims the run wrote among them, every entry of it true of that text, and nothing the reply says about the claims contradicts a finding the same reply states. Everything the reply says about the text is true of the text it names, and a statement about the text as it arrived says so. Where the delivered text differs from the text as it arrived, the account closes with one paragraph saying by kind what the run changed beyond the claim account, without itemising it. Internal review reasoning is not output.

## POSITIONAL ARGUMENTS

*TEXT*|*PATH*|*URL*

The single text to review, supplied inline, as a local path, or as a URL. When omitted, the current turn must identify it. In-place editing requires *PATH*.

## OPTIONS

**--genre**=*GENRE*

Select an installed genre. The default is `general`; an unknown genre is refused.

<!-- kntnt:editorial-genres -->

**--technique**=*TECHNIQUE*

Select an installed structural technique. Where none is named here, in the selected brief's or the text's `kntnt` map, in an instruction, or in applicable conversation context, the resolved genre's ordinary technique applies. To review against no technique, say so in an instruction or carry `technique: none` in the map: this flag takes an installed name and cannot say none. Resemblance never selects one.

<!-- kntnt:editorial-techniques -->

**--language**=*LANGUAGE*

Select the language or locale by canonical code, case or separator variant, curated alias, or ordinary description. It overrides every other source and is passed to `proofread`.

**--brief=**_PATH|URL_

Review against the Writing Brief at this path or URL as well as the editorial contract. The brief is never edited, proofread or delivered. A Contextual Instruction or applicable Conversation Context can also name it; the option wins over the instruction, which wins over conversation. A brief merely present in the session is not selected.

**--max**=*N*

Set the maximum number of substantive corrections. It accepts any non-negative integer and defaults to `1`. `0` only reviews and reports; the final mechanical pass still runs.

**--output**=*TARGET*

Deliver to `response` (the default) or one filesystem path. A new path creates a file, an existing file is replaced, and an existing directory receives a derived non-colliding filename. It cannot be combined with **--in-place**, name the source path, or replace the selected brief's file (including an alias of that file).

**--in-place**[=**on**|**off**]

Replace the writable local source file. Bare **--in-place** means `on`; accepted values are `yes`, `on`, `true`, `no`, `off`, and `false`. Inline text, URLs, uploaded or read-only sources, simultaneous **--output**, and replacement of the selected brief's file are refused.

## DIAGNOSTICS

An invalid form is refused rather than repaired or ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/redline --help`. A flag is refused rather than ignored where it has no work to do here.

Refusals include unknown, missing, repeated, or out-of-order input; unsupported resources; invalid budgets; multiple texts; incompatible output options; unsafe in-place sources; and unwritable destinations. This is the whole of what is refused over the form of an invocation.

An unreadable selected brief stops the run before review or writing; it is never silently ignored. Missing material referenced by a readable brief is reported as a limitation and the affected shortfall is left for the writer.

Other stops are documented with the value they concern, under `## INVOCATION ENVELOPE`, and under `## DEPENDENCIES`.

A valid text is reviewed even when it is a brief, outline, or notes. Its incompleteness becomes a finding, not a refusal.

Unsupported winning `kntnt` metadata stops the run unless a flag overrides it. Mixed or ambiguous language produces one question before anything is written.

## EXAMPLES

**/redline --brief=brief.md --output=reviewed.md draft.md**

Review `draft.md` against the editorial contract and `brief.md`, then deliver the text with a question-by-question brief report.

**/redline draft.md -- Review it against the brief in brief.md.**

Select the brief through the Contextual Instruction. An earlier conversation instruction naming the brief for this review also works when neither the option nor this instruction selects one.

**/redline article.md**

Review `article.md`, allow one correction, proofread the result, and return it without changing the file.

**/redline --max=0 article.md**

Report editorial findings without correcting them; the final mechanical pass still runs.

**/redline --genre=pressrelease --language=sv --in-place utkast.md**

Review and replace `utkast.md` as a Swedish press release.

**/redline --technique=abt --output=~/reviewed draft.md**

Apply the ABT technique and deliver a non-colliding file under `~/reviewed`.

**/redline --genre=report --max=0 handoff.md -- Review it as a PAC piece in Swedish.**

Review `handoff.md` as a report without substantive correction. If its `kntnt` map already settles technique and language, the Contextual Instruction is suppressed and the review still runs.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv`; the Kntnt Manager, whose Collection Library carries the editorial contract, the genres and techniques, the anti-slop catalogue, and the language resources this Skill resolves against; the `proofread` Skill, which performs the closing mechanical pass; and a harness that can run subagents, which stays a requirement whatever Correction Budget an invocation names. An unavailable subagent capability stops the invocation before anything is reviewed or written.

## SEE ALSO

**/write**, **/proofread**, **/kntnt select**
