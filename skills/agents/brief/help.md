# brief

## NAME

brief - keep this conversation's replies concise and decision-relevant

## SYNOPSIS

**/brief** (**on**|**off**) [**--** *INSTRUCTION*]

**/brief** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`on` adopts the Brief perspective for later replies: it leads with the conclusion, keeps practical implications, decisions, and required user actions, and drops the narration around them. `off` drops the perspective again. Neither revisits the preceding answer, and an explicit request for detail overrides the mode for that reply.

The state belongs to the conversation it is typed in and to nothing else. It holds until `off` or until that conversation ends, and it is never observable in another window, another project, or a later session — two conversations open on the same project hold independent states, and `status` is how you ask which one you are sitting in.

Nothing is written anywhere. There is no settings key, no style file, and no state on disk, in any Harness: the mode lives in this conversation and ends with it, leaving nothing behind. A standing default across sessions is the user's own configuration rather than this Skill's business.

The mode takes effect on the turn it is typed, so the report of the change already obeys it.

The Skill takes no free-text operand and declares no flag. Put any guidance about the run after `--`, as `/brief on -- svara på svenska`.

Brief mode affects conversation replies, not code, documentation, commit messages, or other artifacts.

## COMMANDS

**on**

Adopt the Brief perspective for the rest of this conversation.

**off**

Drop the Brief perspective for the rest of this conversation.

**status**

Report whether the perspective is on or off in this conversation, without changing anything.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the most specific SYNOPSIS, changes nothing, and points to that page. A flag is refused rather than ignored where it has no work to do here: this grammar declares no flag at all, so every `--`-prefixed token is undeclared and refused as one, and so is any token that does not open a recognized command path.

A command path is required. A bare **/brief**, a second command path, and unseparated text are each an invalid form.

## EXAMPLES

**/brief on**

Keep later replies in this conversation concise and decision-relevant, leaving the preceding answer untouched.

**/brief status**

Report whether this conversation is currently in Brief mode.

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

None.

## SEE ALSO

**/brief on --help**, **/brief off --help**, **/brief status --help**, **/tldr --help**, **/delegation --help**, **/kntnt select**
