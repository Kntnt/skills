# write

## NAME

write - turn a brief and its source material into one first draft

## SYNOPSIS

**/write** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--frontmatter**=*BOOLEAN*] [**--output**=*TARGET*] [*BRIEF*] [**--** *INSTRUCTION*]

## DESCRIPTION

`write` turns a brief and its source material into one first draft. It does not review or proofread the result.

Sources may be inline text, local files, URLs, the Contextual Instruction, or Conversation Context. Several sources may feed one draft. Supplying a file does not select an output; the response is the default.

Genre, technique, language, and output resolve independently before writing. Genre defaults to `general`, and language to the request and material. Where nothing names a technique, the resolved genre supplies the one that kind of text is ordinarily written with, and a genre naming none leaves the draft with none. The delivery says which technique was resolved and where it came from. Ambiguous or mixed language produces a question.

The draft follows the base editorial contract, resolved genre, optional technique, and resolved language's composition guidance. It uses no review, anti-slop, or mechanics guidance.

Every claim must be supported by the supplied material. Attribution, uncertainty, scope, chronology, and causality are preserved; uncertain quotations are paraphrased.

Handoff Metadata is added by default so a later review can reuse the resolved genre, technique, and language.

## POSITIONAL ARGUMENTS

*BRIEF*

What to write and which sources to use, in any language. It may be omitted when the Contextual Instruction or conversation already supplies the brief. An invocation with no usable brief or material is refused.

## OPTIONS

**--genre**=*GENRE*

Select an installed genre by filename without its extension. The default is `general`; an unknown genre is refused.

**--technique**=*TECHNIQUE*

Select an installed structural technique. Where none is named here, in the material's `kntnt` map, in an instruction, or in applicable conversation context, the resolved genre's ordinary technique applies. To write without one, say so in an instruction or carry `technique: none` in the map: this flag takes an installed name and cannot say none. A technique is never inferred from resemblance.

**--language**=*LANGUAGE*

Select the output language by canonical code, curated alias, or ordinary description. Case and separator variants are accepted. Without the option, the request and material determine the language.

**--frontmatter**=*BOOLEAN*

Control Handoff Metadata. Accepted values are `yes`, `on`, `true`, `no`, `off`, and `false`; the default is on. Turning it off removes only the Kntnt map.

**--output**=*TARGET*

Deliver to `response` (the default) or one filesystem path. A new path creates a file, an existing file is replaced, and an existing directory receives a derived filename. A source path cannot also be the output.

## RESOLUTION

Each parameter resolves from the Formal Invocation, a recognized `kntnt` frontmatter map, the Contextual Instruction, Conversation Context, inference, and finally its default; the technique has one level more, the resolved genre's ordinary technique, just above that default. The first value found wins for that parameter only.

A Contextual Instruction every higher level has already settled is suppressed rather than refused: the run continues, and the delivery names the suppressed instruction beside the resolved configuration where saying so is useful.

Only `genre`, `technique`, and `language` under a leading `kntnt` map are configuration. Ordinary frontmatter and output settings are not. Unsupported map values stop the run unless the Formal Invocation overrides them.

## SOURCE FIDELITY

Every claim must be supported by the supplied material. Attribution, uncertainty, scope, chronology, and causality are preserved.

A requested length limits selection; it never licenses invention. When the material is insufficient, the draft is shorter and the response names what is missing.

Spoken syntax, fillers, and searching repetition may be repaired inside quotations. Meaning, stance, certainty, distinctive wording, and self-corrections are preserved. Doubtful quotations are paraphrased with attribution.

Quotation approval remains a human responsibility.

## HANDOFF METADATA

The map records the resolved genre, technique or `none`, and canonical language code:

```
---
kntnt:
  genre: general
  technique: none
  language: en_GB
---
```

The map is merged into existing frontmatter. It never embeds the invocation, sources, or options. A later run reads `technique: none` as no technique rather than as a missing value, so a draft written without one is reviewed without one.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, points to `/write --help`, and leaves no output. A flag is refused rather than ignored where it has no work to do here.

Refusals include unknown, missing, repeated, or out-of-order input; unsupported resources; invalid booleans; unwritable or source-equal output; and an invocation with nothing to write.

Mixed or ambiguous language produces a question before writing.

## EXAMPLES

**/write draft a short note for the team from notes.md**

Create one draft in the response with the general genre and Handoff Metadata.

**/write --language=sv --output=./drafts/ interview.md and background.md**

Create a Swedish draft from two sources and deliver it under `./drafts/`.

**/write --frontmatter=no summarise https://example.org/report for a newsletter**

Create a draft without a Kntnt map.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

Requires `uv` and the Manager, whose Collection Library carries the editorial contract, the genres and techniques, the Language Resources, and the resolver that selects among them. No peer Skill and no Harness Capability beyond reading the material you supply.

## SEE ALSO

**/kntnt select**
