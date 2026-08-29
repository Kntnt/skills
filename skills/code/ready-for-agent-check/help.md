# ready-for-agent-check

## NAME

ready-for-agent-check - find ticket defects that would stop an unattended builder

## SYNOPSIS

**/ready-for-agent-check** [*TICKET*...] [**--** *INSTRUCTION*]

## DESCRIPTION

`ready-for-agent-check` reads each ticket in an isolated subagent context that did not help write it and asks whether an unattended builder could complete it without stopping for information or judgement. It reports advice and changes neither the tracker nor the Project.

Each reviewer receives the ticket's complete thread: the original body followed by every comment in chronological order with author and date. Later comments override conflicting earlier text, and acceptance criteria added in comments remain criteria. The reviewer receives no explanation or intent from the invoking session.

The reviewer also checks ticket claims against the current Project. Stale paths, symbols, line references, reserved identifiers, enumerations, and other repository facts are reported beside the current state.

## POSITIONAL ARGUMENTS

*TICKET*...

One or more bare ticket references such as `#12`. When omitted, the Skill checks every open ticket carrying `ready-for-agent`. Named tickets are checked regardless of label so the result can inform whether they should receive it.

A reference that does not resolve, is not a number, or uses the cross-repository form `owner/repo#number` makes the complete invocation invalid.

## REVIEW CRITERIA

**Open decision**

The ticket presents alternatives without choosing one, defers a value to a person, or asks the builder to decide without granting that authority.

**Unevaluable condition**

The work branches on a condition the builder cannot determine from the ticket and Project.

**Indeterminate criterion**

An acceptance criterion has no observable pass or fail outcome.

**Stale claim**

The current Project no longer supports a path, symbol, line, identifier, count, or other fact asserted by the ticket.

**Missing fact**

The ticket requires a command, convention, term, or source it neither carries nor locates.

**Open scope**

The work has no closing boundary or its scope contradicts its acceptance criteria.

**Human-owned work**

Completion requires product judgement, external authority, a deferred design decision, or a check only a person can perform.

## OUTPUT

The report gives each ticket one verdict: whether a builder could carry it from start to finish. It then lists every finding under two classes.

**Stops**

Conditions a builder cannot pass without asking. Each finding quotes the relevant ticket text, states the question it creates, and names what the ticket must settle.

**Costs**

Conditions a builder can pass only by reconciling stale information, resolving ambiguity twice, or finding omitted facts.

There is no partial pass. An uncertain reviewer returns no, because uncertainty can stop an unattended run.

## DIAGNOSTICS

The Skill accepts ticket references and no options. Every option and invalid reference is refused rather than ignored; it names the error, prints the SYNOPSIS, checks nothing, and points to `/ready-for-agent-check --help`.

An empty resolved scope is a successful no-op and is reported as such.

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

**Binaries**

`gh` and `uv` on `PATH`. `gh` must be authenticated for read access to the current Project's repository.

**Skills**

The Manager must be Enabled so the dependency check can run.

**Capabilities**

The current Harness must be able to spawn subagents. Reviewing in the context that helped write the ticket is not a degraded mode; the Skill stops when this Capability is Unsatisfied.

## SEE ALSO

**/orchestrate --help**, **/kntnt select**
