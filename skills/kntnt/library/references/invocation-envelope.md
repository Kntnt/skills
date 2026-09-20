# The Invocation Envelope

The contract every Skill of this collection meets before it reads an argument of its own: how the reserved separator splits an Invocation Envelope, what a Contextual Instruction may and may not settle, the two refusals a bad Envelope or a bad Formal Invocation takes, and how a caller recovers from its own construction error. It is stated here once and executed by every Skill. A Skill's body follows this file, and its manpages point a reader at it; none of them restates it.

## The separator

`[**--** *INSTRUCTION*]` introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

The split happens before help routing and before formal validation, and only the Formal Invocation reaches Help, the Skill's own argument grammar, its scripts, and any nested formal parser.

## Quoting a value

An operand and a flag value each arrive without the outer quotes they were written in — `"a b"` and `'a b'` are both the value `a b` — the pair being the caller's way of holding spaces together rather than part of what was written. Only a value whose own quoted run closes at its last character loses that pair, so an inner quote is kept (`'say "hi"'` is `say "hi"`), and a value that is two runs beside each other, a run closed early, a backtick-quoted run, or an unbalanced quote keeps every mark it carries. This happens after the split above, which it never moves: `"--"` is formal data exactly as stated there, and is the value `--`.

## What a Contextual Instruction may settle

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

## The two refusals

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

The addressed page is the most specific recognized command page — the Skill's own `help.md` where no command path was recognized — and the refusal points at that page's own `--help` route rather than at the Skill's root route.

The engine refuses every invalid form and never repairs or ignores one. When the user supplied the invalid form, the caller reports that refusal without repairing, reordering, discarding, or reinterpreting the user's syntax. A flag is refused rather than ignored where it has no work to do, an operand written before a flag is refused rather than reordered, and an incomplete form is refused rather than asked about — because a flag accepted and ignored teaches that flags sometimes do nothing, a form silently repaired teaches an order the Skill does not accept, and a question asked in place of the grammar leaves the user guessing at what the grammar is.

## A caller's construction error

When the caller introduced a known error while forwarding valid user input or constructing a nested invocation, and knows a valid correction that preserves the user's request and authority, it corrects its construction, submits the corrected invocation through the normal validation path, and continues from the failed boundary. The corrected construction preserves every resolved option, the complete artifact, and the authorised destination. Completed work is retained: a refusal before the called operation starts spends no substantive correction, budget round, or actual pass.

Recovery requires that diagnosis and valid correction. An exit status alone never authorises a retry. Exact help, invalid user input, an unmet dependency, an unrelated failure, and a failure whose origin or valid correction is unknown keep their applicable handling; the caller reports the actual blocker instead of guessing or repeating the same failed call.

Before resuming an operation that may already have produced effects, the caller establishes what completed and resumes only what remains. It never replays a completed external action, widens permissions or the task, changes the authorised destination, or skips validation. Where the partial outcome cannot be established, it reports that uncertainty and stops.

## A nested Skill

A nested Skill receives only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; an outer instruction is never forwarded blindly. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

## Worked cases

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
