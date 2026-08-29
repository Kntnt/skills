# write

## NAME

write - turn a brief and its source material into one first draft

## SYNOPSIS

**/write** [**--genre**=*GENRE*] [**--technique**=*TECHNIQUE*] [**--language**=*LANGUAGE*] [**--frontmatter**=*BOOLEAN*] [**--output**=*TARGET*] [*BRIEF*] [**--** *INSTRUCTION*]

## DESCRIPTION

`write` turns a brief and its source material into one first draft. It does not review or proofread the result.

Sources may be inline text, local files, URLs, the Contextual Instruction, or Conversation Context. Several sources may feed one draft. Supplying a file does not select an output; the response is the default.

Genre, technique, language, and output resolve independently before writing. Genre defaults to `general`, technique defaults to none, and language defaults to the request and material. Ambiguous or mixed language produces a question.

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

Select an installed structural technique. There is no default, and a technique is never inferred from resemblance.

**--language**=*LANGUAGE*

Select the output language by canonical code, curated alias, or ordinary description. Case and separator variants are accepted. Without the option, the request and material determine the language.

**--frontmatter**=*BOOLEAN*

Control Handoff Metadata. Accepted values are `yes`, `on`, `true`, `no`, `off`, and `false`; the default is on. Turning it off removes only the Kntnt map.

**--output**=*TARGET*

Deliver to `response` (the default) or one filesystem path. A new path creates a file, an existing file is replaced, and an existing directory receives a derived filename. A source path cannot also be the output.

## RESOLUTION

Each parameter resolves from the Formal Invocation, a recognized `kntnt` frontmatter map, the Contextual Instruction, Conversation Context, inference, and finally its default. The first value found wins for that parameter only.

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

The map is merged into existing frontmatter. It never embeds the invocation, sources, or options.

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

Requires `uv` and the Manager, whose Collection Library carries the editorial contract, the genres and techniques, the Language Resources, and the resolver that selects among them. No peer Skill and no Harness Capability beyond reading the material you supply.

## SEE ALSO

**/kntnt select**
