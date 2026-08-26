# write

## NAME

write - turn a brief and its source material into one first draft

## SYNOPSIS

**/write** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--frontmatter**=*BOOLEAN*] [**--output**=*TARGET*] [*BRIEF*] [**--** *INSTRUCTION*]

## DESCRIPTION

`write` turns a direct brief into one first draft and stops there. It reviews nothing afterwards, proofreads nothing, and invokes no other Skill: running an editorial pipeline over a draft is a separate choice, made after reading the draft rather than instead of reading it.

The material may be anything the Harness can reach. Text pasted into the invocation, local files, URLs, guidance given after the reserved separator, and material already in the conversation are all usable, and several of them may feed one draft — an interview transcript and its background reading can stay where they already are. Supplying a file selects no destination: by default the draft comes back in the response and nothing on disk changes.

The genre, the technique, the language, and where the result goes are all settled before a word is written. Each is resolved on its own, by the precedence under `RESOLUTION`, so an explicitly named genre sits happily beside a language taken from the conversation. Genre defaults to `general`, which is a complete contract rather than the absence of one. No technique applies unless one was selected. The language defaults to the language of the request and the material, and material too mixed to settle is a question rather than a guess.

What the draft is written against is deliberately small: the Collection's base editorial contract, the selected genre, the selected technique where there is one, and the composition guidance of the resolved language. Review, anti-slop, and mechanics guidance belong to the Skills contracted to act on them and are not loaded here.

The draft is answerable to its material. `write` invents no facts, and attribution, uncertainty, scope, chronology, and causality survive into the text as the material has them. Spoken quotations may be repaired within a narrow boundary — see `SOURCE FIDELITY` — and where fidelity is doubtful the draft paraphrases rather than manufacturing a quotation.

By default the delivered artifact carries Handoff Metadata, a small reserved map in leading YAML frontmatter recording what this run resolved, so that a later review can recover the configuration cheaply. It is one option to turn off.

## POSITIONAL ARGUMENTS

*BRIEF*

Free text in any language, saying what to write and pointing at whatever the draft should be built from — a path, a URL, or a passage pasted in whole. It may be omitted where the conversation or an instruction after the reserved separator already carries the brief; an invocation with no brief, no material, and no applicable guidance has nothing to write and is refused.

## OPTIONS

**--genre**=*GENRE*

The kind of text to write, named as an installed genre. Defaults to `general`. The installed genres are the resources in the Collection Library's editorial `genres/` directory, and the value is a resource's filename without its extension; a value naming no installed resource is refused rather than falling back to the default.

**--technique**=*TECHNIQUE*

A structural technique the draft has to satisfy, named as an installed technique and resolved the same way as a genre. There is no default: a technique applies because it was selected, and is never inferred from a draft's or a source's resemblance to one.

**--language**=*LANGUAGE*

The language to write in. Accepts a canonical code such as `sv` or `en_GB`, a curated alias such as `BrE` or `brittisk engelska`, or a description in words, which is interpreted and then verified against what is installed. Case and separators carry no meaning, so `en-GB` and `EN_GB` reach the same resource. Without it, the language is the language of the request and the supplied material.

**--frontmatter**=*BOOLEAN*

Whether to attach Handoff Metadata. Accepts `yes`, `on`, or `true` and `no`, `off`, or `false`; the default is on. Turning it off suppresses the reserved Kntnt map alone and never the frontmatter the requested artifact itself needs.

**--output**=*TARGET*

Where the draft goes: the keyword `response`, which is the default, or one filesystem path. A path that does not exist is created; a path naming an existing file is overwritten, naming it being the authorization; a path naming an existing directory receives a file whose name is derived from the source or the working title. A path equal to a local file that supplied material is refused — this Skill creates a text and never replaces the material its brief came from.

## RESOLUTION

Genre, technique, language, and the output options are each resolved independently, in this order: the Formal Invocation; a recognized Kntnt map in the leading frontmatter of supplied material; the current Contextual Instruction; applicable Conversation Context; inference from what was requested and supplied; then the parameter's default. A value found at one level suppresses the levels below it for that parameter alone, never for the others. A Contextual Instruction every higher level has already settled is suppressed rather than refused: the run continues, and the delivery names the suppressed instruction beside the resolved configuration where saying so is useful.

A recognized Kntnt map is the reserved `kntnt` key and its `genre`, `technique`, and `language` values. Ordinary document frontmatter is never read as configuration, whatever its keys are called, and the map never carries output options. A map whose value cannot be used — a language code the Collection does not carry, a genre or technique that is not installed — is reported as unusable artifact metadata rather than quietly read as something near it, unless the invocation already settled that parameter itself.

## SOURCE FIDELITY

Every claim in the draft is supported by the supplied material, and attribution, uncertainty, scope, chronology, and causality are preserved. Nothing is added because it would round the text off.

A length the brief asks for is a constraint on how much of the material to use, not a licence to add to it. Where the material cannot fill it, the draft comes back at the length the material supports and the reply says what further material would close the gap.

Inside a direct quotation, spoken syntax, fillers, and searching repetition may be repaired. Meaning, stance, certainty, distinctive wording, and a speaker's own self-correction may not, and nothing is added. Where fidelity is uncertain, the draft paraphrases with careful attribution instead of assembling a quotation that sounds better than the material supports.

Whether a quoted person has approved their quotation is a human arrangement. Nothing here verifies it or stands in for it.

## HANDOFF METADATA

The attached map carries exactly three normalized values — the resolved genre, the resolved technique or `none`, and the canonical language code — under a reserved `kntnt` key in leading YAML frontmatter:

```
---
kntnt:
  genre: general
  technique: none
  language: en_GB
---
```

Where the artifact needs frontmatter of its own, the map is merged into it rather than written as a second block. The invocation's raw argument, the source material, and the options this run was given are never embedded.

## DIAGNOSTICS

An incomplete or invalid form is refused rather than ignored, and a flag with no work to do here is refused rather than accepted and forgotten. The refusal names what was wrong, prints the SYNOPSIS, points to `/write --help`, and leaves nothing behind: no file created, none overwritten, and no draft half-delivered.

The cases are an unknown option, an option written without a value, an option repeated, a boolean outside its vocabulary, a genre or technique that is not installed, a language selector that reaches no installed resource or more than one, a destination that cannot be written, an output path equal to a file that supplied material, an invocation with nothing to write, and a brief written before an option rather than after every option.

A materially ambiguous or mixed language is a question rather than a refusal: the candidates are named and the run waits, because writing in a guessed language wastes the draft rather than the invocation.

## EXAMPLES

**/write draft a short note for the team from notes.md**

One draft in the response, in the language of the brief and the notes, with the general genre and Handoff Metadata attached.

**/write --language=sv --output=./drafts/ interview.md and background.md**

One Swedish draft built from two sources, delivered into an existing directory under a filename derived from the source, without overwriting anything already there. Naming an installed genre or technique alongside is what makes the draft that kind of text.

**/write --frontmatter=no summarise https://example.org/report for a newsletter**

A draft carrying no Kntnt map, for a destination whose own frontmatter conventions are not this Skill's business.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

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

Requires `uv` and the Manager, whose Collection Library carries the editorial contract, the genres and techniques, the Language Resources, and the resolver that selects among them. No peer Skill and no Harness Capability beyond reading the material you supply.

## SEE ALSO

**/kntnt select**
