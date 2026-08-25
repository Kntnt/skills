# unslop

## NAME

unslop - apply the anti-slop pass alone to one text and change nothing else

## SYNOPSIS

**/unslop** [**--language**=*LANGUAGE*] [**--max**=*N*] [**--output**=*TARGET*] [*TEXT*|*PATH*|*URL*] [**--** *INSTRUCTION*]

**/unslop** [**--language**=*LANGUAGE*] [**--max**=*N*] **--in-place**[=**on**|**off**] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

`unslop` reads one text against this collection's anti-slop catalogue, repairs what that pass found as far as its Correction Budget reaches, reports whatever is left, and stops. It is one lens applied on its own, meant for a text that is otherwise finished: the argument is settled, the structure is right, and what is wrong is that the prose sounds like a machine wrote it.

What the pass looks for is the seven patterns the catalogue carries. A false contrast rejects a position nobody held before stating the actual claim. An empty opening announces the subject or asserts that it matters instead of starting. Importance inflation asserts weight the material has not shown. Vague attribution credits a claim to nobody. Synonym cycling gives one thing a new name every time it is mentioned. Robotic rhythm builds every sentence and paragraph to the same template. A generic conclusion restates what the reader has just read or reaches for an uplifting abstraction. Each is applied by what it does in the text's own language — the catalogue's examples are English because it is, and they are read as semantic patterns rather than matched as strings, with a language's own slop words, phrases, punctuation, and constructions coming from that language's own guidance.

Nothing else is loaded, and nothing else is corrected. No base contract, no genre, no technique, and none of the wider guidance a language resource carries: this Skill reads no more than it may act on, and a sentence you would have put differently, a structure you would have chosen against, or a fact you would have checked is not a finding here. Applying the whole editorial contract is `redline`'s gesture, and this Skill can neither replace it nor grow into it.

Mechanical errors are somebody else's gesture too. `unslop` runs no closing pass over spelling, grammar, punctuation, or the locale's own conventions, and it needs no other Skill to be installed. Run `proofread` on the result for those: a text that still has a typo after this pass was never going to have it removed here.

No provenance is required. A text this collection wrote, a text a person wrote, and a text produced somewhere else entirely are all read the same way. The language is the one editorial parameter this Skill resolves, and it takes the first of these that answers: the **--language** value, a `language` value in a `kntnt` map in the text's own leading frontmatter, the Contextual Instruction, applicable Conversation Context, and then the language of the text itself, which is also the default. A text whose language is materially ambiguous or mixed — no dominant language, or alternation inside paragraphs — is asked about rather than guessed at.

Ordinary document frontmatter is never configuration. A `language`, `lang`, `genre`, or `technique` key sitting at the top level of a document's own frontmatter belongs to that document, and only a `kntnt` map is read as this collection's. No such map is created and none is brought into line with what the run resolved: this Skill settles one of the three values such a map records, so writing one would claim a configuration it never resolved. Where a map carries a language no installed resource answers to, and no **--language** value supersedes it, the run reports unusable artifact metadata and stops rather than reading it as the code it resembles.

Source material is outside the contract. The pass judges what is in front of it and never asks for the interview, the brief, or the research a text was written from — it neither compares the text against them nor remarks that it could not. Checking a text against the material it came from belongs to the Skill that wrote it.

The Correction Budget bounds how many corrections this pass may delegate. It is any non-negative integer and **defaults to one**, so an ordinary run buys one correction and one chance to verify it. A budget of zero reads and reports without correcting, leaving the findings for you to act on. A larger number bounds a longer loop, and it bounds rather than requires — a text with nothing left to correct stops with the rest of the budget unspent.

Every correction is made by a subagent started fresh for it, carrying no earlier findings and no earlier attempt, so the framing of one round cannot bias the next. It is given the complete current text, the complete findings of the most recent pass, the resolved language, and the requirement to leave alone everything those findings do not concern. What comes back is then read again from the top rather than believed: an agent reporting on its own repair is the one reader who cannot check it. The loop stops when no findings remain, when a correction makes no relevant progress — the findings it was given still standing with nothing they named changed — or when the budget is spent, and the last two deliver the text with the findings that are left, marked as unresolved, for you to finish.

Repairs are the smallest change that removes the pattern. The writer's vocabulary, bluntness, humour, admitted uncertainty, and rhythm are what makes a text theirs, and a pass that tidied all of it into even prose would have replaced one machine voice with another. A weak closing metaphor is removed rather than improved upon, a strong sentence is left alone even where it is unusual, and where a phrase is doing real work — a hedge marking genuine doubt, a repetition that lands — the pattern is not present and nothing changes.

One invocation processes one text. Several paths, a glob reaching more than one file, or a directory of texts is refused rather than resolved into a configuration per file, because the language, the destination, the findings, and any replacement of a source are settled once and for one text.

Delivery changes nothing on disk unless it is asked to. The default target is the response; **--output** names a file or an existing directory, and **--in-place** replaces the single writable local file the text came from. A run with findings left delivers the text to that target and reports the findings separately, whether or not anything in the text changed, and a run aimed at a file leaves the findings in the response beside it. A clean run delivers the text alone, and a clean run aimed at the response or at its own source that changed nothing writes nothing and returns a short no-change status in the text's own language.

The pass's own working is not output. The reasoning behind a finding, the passages weighed and dismissed, and anything exchanged with a correction subagent stay inside the run; what comes back is the text and, where any remain, the findings.

A model never starts this Skill on its own. *This text reads like AI* is a judgement about how prose sounds, and it is the author's to make: a model reaching for a rewrite on that judgement unasked would be deciding something nobody asked it to decide. Typing `/unslop` is the whole of the trigger.

## POSITIONAL ARGUMENTS

*TEXT*|*PATH*|*URL*

The text to read, supplied inline, as one local path, or as one URL. Omitted, it is the single text the current turn identifies. In-place editing requires the *PATH* form.

## OPTIONS

**--language**=*LANGUAGE*

The language or locale whose anti-slop guidance applies. It accepts a canonical code (`sv`, `en_GB`), a case or separator variant of one (`en-GB`, `EN_GB`), a curated alias (`BrE`, `brittisk engelska`), or an ordinary description of a language written in any language. It overrides every other source, including a `kntnt` map in the text's frontmatter. Without it the precedence in DESCRIPTION applies, ending at the language of the text itself.

**--max**=*N*

The Correction Budget: the greatest number of corrections this pass may delegate. It takes any non-negative integer and defaults to `1`. `0` reads and reports without correcting; a larger number is a ceiling rather than a quota, and a run that has nothing left to correct stops with the rest unspent. A negative, non-integral, or otherwise malformed value is refused before anything is read or written.

**--output**=*TARGET*

Where the resulting text is delivered. `response` is the default and states that default explicitly; any other value is one filesystem path. A path that does not exist creates exactly that file, a path naming an existing file replaces it without asking for a second confirmation, and a path naming an existing directory receives a filename derived from the source, never overwriting what is already there. It cannot be combined with **--in-place**, and naming the source's own path is refused in favour of **--in-place**.

**--in-place**[=**on**|**off**]

Replace the file the text came from with the result. It accepts `yes`, `on`, and `true` against `no`, `off`, and `false`; bare **--in-place** means `on`, and `off` is both the default and the value that has the same effect as omitting the option. It requires exactly one writable local file and is refused for inline text, a URL, an uploaded or read-only source, and for any invocation that also names an output.

## DIAGNOSTICS

An incomplete or invalid form is refused rather than repaired or ignored. The Skill names in one line what was wrong, prints the SYNOPSIS, reads nothing, writes nothing, and points at `/unslop --help`. A flag with no work to do is refused rather than ignored, an accepted and ignored flag teaching that flags sometimes do nothing.

Refused before any side effect, so that nothing is left half done: an undeclared flag, a text written before a flag rather than after every flag, a missing or invalid option value, an option given twice, a language selector reaching no installed resource or more than one, a Correction Budget that is not a non-negative integer, more than one text in one invocation, **--output** together with **--in-place**, an output path equal to the input path, in-place editing of inline text, a URL, or a read-only or non-local source, and a destination whose parent directory does not exist.

A `kntnt` map naming a language that is neither a canonical code nor an installed alias, where no **--language** value supersedes it, is reported as unusable artifact metadata. The run stops rather than reinterpreting the value, so a spelling such as `en_UK` never quietly becomes `en_GB`.

A text whose language cannot be settled — mixed, or a description matching no installed resource uniquely — produces one question rather than a guess. Nothing has been written at that point, so the question costs nothing to answer either way.

## EXAMPLES

**/unslop article.md**

Read `article.md` against the anti-slop catalogue in its own language, delegate one correction for what the pass found and read the result again to verify it, and return it in the response with any findings still unresolved beside it. `article.md` itself is left alone, and nothing about its spelling or punctuation is touched.

**/unslop --max=0 article.md**

Report what the pass found in `article.md` and correct nothing, leaving the findings for you to act on yourself.

**/unslop --language=sv --max=3 --in-place utkast.md**

Read `utkast.md` against the Swedish anti-slop guidance, allow up to three corrections with a re-reading after each, and replace the file with the result. Findings, where any remain, come back in the response.

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

`uv`; the Kntnt Manager, whose Collection Library carries the anti-slop catalogue and the language resources this Skill resolves against; and a harness that can run subagents, which stays a requirement whatever Correction Budget an invocation names. No other Skill.

## SEE ALSO

**/redline**, **/proofread**, **/write**, **/kntnt select**
