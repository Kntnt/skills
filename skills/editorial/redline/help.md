# redline

## NAME

redline - review one text against the editorial contract, correct what it finds, and close with one mechanical pass

## SYNOPSIS

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--max**=*N*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/redline** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--max**=*N*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`redline` reads one text against this collection's editorial contract, repairs what the review found as far as its Correction Budget reaches, reports whatever is left, and finishes with exactly one mechanical pass. What it reads the text against is the base contract, the selected genre, the optional technique, the shared anti-slop catalogue, and the composition, review and anti-slop guidance of the resolved language — each with the diagnostic half a reviewer needs on top of the half a draft is written to.

No provenance is required. A text this collection wrote, a text a person wrote, and a text produced somewhere else entirely are all reviewed the same way. Where a text carries a `kntnt` map in its leading frontmatter, that map supplies defaults and is brought into line with what the run resolved; where it carries none, none is added, and a text without one is never worth less to this Skill than a text with one.

Genre, technique and language are resolved independently, each taking the first of these that answers: the invocation, a `kntnt` map in the text's own frontmatter, the Contextual Instruction, applicable Conversation Context, inference from the text, and then the default — the general genre, no technique, and the language of the text itself. A value found at one level suppresses the levels below it for that parameter alone, so an explicit genre sits perfectly well beside a language read out of frontmatter and a technique named in an instruction. A technique is never inferred from a text that merely resembles one, and a text whose language is mixed produces a question rather than a guess.

Ordinary document frontmatter is never configuration. A `language`, `lang`, `genre`, or `technique` key at the top level of a document's own frontmatter belongs to that document, and only a `kntnt` map is read as this collection's. Where such a map names a genre, technique, or language nothing here installs, and no flag supersedes it, the run reports unusable artifact metadata and stops rather than reading it as the value it resembles.

Source material is outside the contract. The review judges what is in front of it and never asks for the interview, the brief, or the research a text was written from — it neither compares the text against them nor remarks that it could not. A contradiction, an unsupported claim, or an editorial defect visible inside the text itself remains an ordinary finding. Checking a text against the material it came from belongs to the Skill that wrote it.

The mechanical pass is last and happens once. After the review and whatever correction it led to, `redline` runs `proofread` on the resulting text with the resolved language supplied explicitly, and nothing substantive follows it — running it last is what keeps a later edit from putting mechanical errors back into a text that was just cleaned of them. Only guidance relevant to mechanical correction is passed on; the genre, the technique, the Correction Budget, and unrelated outer context are not.

The Correction Budget bounds how many substantive corrections a review may delegate. It is any non-negative integer and **defaults to one**, so an ordinary review buys one correction and one chance to verify it. A budget of zero reviews without correcting: the findings come back for you to act on, and the closing mechanical pass still happens. A larger number bounds a longer loop, and it bounds rather than requires — a text with nothing left to correct stops with the rest of the budget unspent.

Every correction is made by a subagent started fresh for it, carrying no earlier findings and no earlier attempt, so the framing of one round cannot bias the next. It is given the complete current text, the complete findings of the most recent review, the resolved genre, technique and language, and the requirement to leave alone everything those findings do not concern. What comes back is then reviewed again from the top rather than believed: an agent reporting on its own repair is the one reader who cannot check it. The loop stops when no findings remain, when a correction makes no relevant progress — the findings it was given still standing with nothing they named changed — or when the budget is spent, and the last two deliver the text with the findings that are left, marked as unresolved, for you to finish.

One invocation processes one text. Several paths, a glob reaching more than one file, or a directory of texts is refused rather than resolved into a configuration per file, because the language, the destination, the findings, and any replacement of a source are settled once and for one text.

Delivery changes nothing on disk unless it is asked to. The default target is the response; **--output** names a file or an existing directory, and **--in-place** replaces the single writable local file the text came from. A run with findings left delivers the text to that target and reports the findings separately, whether or not anything in the text changed, and a run aimed at a file leaves the findings in the response beside it. A clean run delivers the text alone, and a clean run aimed at the response or at its own source that changed nothing writes nothing and returns a short no-change status in the text's own language.

The review's own working is not output. The reasoning behind a finding, the passages weighed and dismissed, and anything exchanged with a correction subagent or a nested Skill stay inside the run; what comes back is the text and, where any remain, the findings.

## POSITIONAL ARGUMENTS

*TEXT*|*PATH*|*URL*

The text to review, supplied inline, as one local path, or as one URL. Omitted, it is the single text the current turn identifies. In-place editing requires the *PATH* form.

## OPTIONS

**--genre**=*GENRE*

The kind of text this is, named by an installed genre resource. `general` is the default and is a complete contract rather than the absence of one. A genre nothing installs is refused rather than falling back to the default.

**--technique**=*TECHNIQUE*

A structural technique the text is held to, named by an installed technique resource. There is no default and none is ever inferred: a technique applies because the invocation, a `kntnt` map, or an instruction selected it, never because the text happens to fall into its shape.

**--language**=*LANGUAGE*

The language or locale whose editorial guidance applies. It accepts a canonical code (`sv`, `en_GB`), a case or separator variant of one (`en-GB`, `EN_GB`), a curated alias (`BrE`, `brittisk engelska`), or an ordinary description of a language written in any language. It overrides every other source, including a `kntnt` map in the text's frontmatter, and it is the language handed to the closing mechanical pass.

**--max**=*N*

The Correction Budget: the greatest number of substantive corrections the review may delegate. It takes any non-negative integer and defaults to `1`. `0` reviews and reports without correcting, still running the closing mechanical pass; a larger number is a ceiling rather than a quota, and a run that has nothing left to correct stops with the rest unspent. A negative, non-integral, or otherwise malformed value is refused before anything is reviewed or written.

**--output**=*TARGET*

Where the resulting text is delivered. `response` is the default and states that default explicitly; any other value is one filesystem path. A path that does not exist creates exactly that file, a path naming an existing file replaces it without asking for a second confirmation, and a path naming an existing directory receives a filename derived from the source, never overwriting what is already there. It cannot be combined with **--in-place**, and naming the source's own path is refused in favour of **--in-place**.

**--in-place**[=**on**|**off**]

Replace the file the text came from with the result. It accepts `yes`, `on`, and `true` against `no`, `off`, and `false`; bare **--in-place** means `on`, and `off` is both the default and the value that has the same effect as omitting the option. It requires exactly one writable local file and is refused for inline text, a URL, an uploaded or read-only source, and for any invocation that also names an output.

## DIAGNOSTICS

An incomplete or invalid form is refused rather than repaired or ignored. The Skill names in one line what was wrong, prints the SYNOPSIS, reviews nothing, writes nothing, and points at `/redline --help`. A flag with no work to do is refused rather than ignored, an accepted and ignored flag teaching that flags sometimes do nothing.

Refused before any side effect, so that nothing is left half done: an undeclared flag, a text written before a flag rather than after every flag, a missing or invalid option value, an option given twice, a genre or technique nothing installs, a language selector reaching no installed resource or more than one, a Correction Budget that is not a non-negative integer, more than one text in one invocation, **--output** together with **--in-place**, an output path equal to the input path, in-place editing of inline text, a URL, or a read-only or non-local source, and a destination whose parent directory does not exist.

That list is the whole of what is refused over the form of an invocation. What a run stops for otherwise is written in the paragraphs below and in the `## INVOCATION ENVELOPE` section. An invocation whose form the list does not name is reviewed, whatever the text turns out to be: a brief, an outline, or notes supplied where the finished piece was expected is read against the resolved genre like any other text, and being that rather than the piece is the review's finding — usually its first — rather than a reason to decline the run or to send you to another Skill.

A `kntnt` map naming a genre, technique, or language nothing installs, where no flag supersedes it, is reported as unusable artifact metadata. The run stops rather than reinterpreting the value, so a spelling such as `en_UK` never quietly becomes `en_GB`.

A text whose language cannot be settled — mixed, or a description matching no installed resource uniquely — produces one question rather than a guess. Nothing has been written at that point, so the question costs nothing to answer either way.

## EXAMPLES

**/redline article.md**

Review `article.md` under the general genre and its own language, delegate one correction for what the review found and review the result again to verify it, proofread that, and return it in the response with any findings still unresolved beside it. `article.md` itself is left alone.

**/redline --max=0 article.md**

Review `article.md` and correct nothing: the findings come back for you to act on yourself, and the closing mechanical pass is still performed.

**/redline --genre=press-release --language=sv --in-place utkast.md**

Review `utkast.md` as a Swedish press release, proofread it in Swedish, and replace the file with the result. Findings, where any remain, come back in the response.

**/redline --technique=abt --output=~/reviewed draft.md**

Review `draft.md` against the ABT technique as well as its genre and deliver the result into the existing directory `~/reviewed`, under a filename derived from the source and never over an existing file.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

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
