# ready-for-agent-check

## NAME

ready-for-agent-check - find ticket defects that would stop an unattended builder

## SYNOPSIS

**/ready-for-agent-check** [*TICKET*...] [**--** *INSTRUCTION*]

## DESCRIPTION

`ready-for-agent-check` reads each ticket in an isolated subagent context that did not help write it and asks whether an unattended builder could complete it without stopping for information or judgement. It reports advice and changes neither the tracker nor the Project.

Each reviewer receives the ticket's complete thread: the original body followed by every comment in chronological order with author and date. Later comments override conflicting earlier text, and acceptance criteria added in comments remain criteria. The reviewer receives no explanation or intent from the invoking session.

The builder it measures against is a Seat no more capable than the reviewer and possibly considerably less: less deliberation, a smaller model, or both. The reviewer's own ease is not the measure, and a fact the reviewer obtained by knowing where to look is reported as a fact the ticket has to locate.

The reviewer also checks ticket claims against the current Project. Stale paths, symbols, line references, reserved identifiers, enumerations, and other repository facts are reported beside the current state.

## POSITIONAL ARGUMENTS

*TICKET*...

One or more bare ticket references such as `#12`. When omitted, the Skill checks every open ticket carrying `ready-for-agent`. Named tickets are checked regardless of label so the result can inform whether they should receive it.

A reference that does not resolve, is not a number, or uses the cross-repository form `owner/repo#number` makes the complete invocation invalid. This grammar declares no flag, so a dash-prefixed token such as `--yes` is a reference like any other, and one that resolves to nothing.

## REVIEW CRITERIA

**Open decision**

The ticket presents alternatives without choosing one, defers a value to a person, or asks the builder to decide without granting that authority.

**Unevaluable condition**

The work branches on a condition the builder could not determine from the ticket or the Project without knowing where to look.

**Indeterminate criterion**

An acceptance criterion has no observable pass or fail outcome.

**Stale claim**

The current Project no longer supports a path, symbol, line, identifier, count, or other fact asserted by the ticket.

**Missing fact**

The ticket requires a command, convention, term, or source that it neither carries nor locates and that the builder could not obtain from the Project without knowing where to look.

**Open scope**

The work has no closing boundary or its scope contradicts its acceptance criteria.

**Human-owned work**

Completion requires product judgement, external authority, a deferred design decision, or a check only a person can perform.

## OUTPUT

The report gives each ticket one verdict: whether a builder could carry it from start to finish. It then lists every finding under two classes. An inference the reviewer had to make to get past a sentence — an intent the ticket does not state, a choice between readings it allows, a fact it neither carries nor locates — is a finding on that sentence and falls under one of those two classes; there is no third.

**Stops**

Conditions a builder cannot pass without asking, the reviewer's own inferences among them where the builder could not have made the same one. Each finding quotes the relevant ticket text, states the question it creates, and names what the ticket must settle.

**Costs**

Conditions a builder can pass only by reconciling stale information, resolving ambiguity twice, or finding omitted facts. Every other inference the reviewer had to make lands here.

There is no partial pass. An uncertain reviewer returns no, because uncertainty can stop an unattended run.

## DIAGNOSTICS

The Skill takes ticket references and no options. It declares no flag and no command path, so a dash-prefixed token is read as a ticket reference rather than as an option, and it is a reference nothing resolves. A reference nothing resolves — a dash-prefixed token, a number the tracker does not know, something that is not a number, the cross-repository form — is refused rather than ignored: the Skill names the reference, prints the SYNOPSIS, checks nothing, and points to `/ready-for-agent-check --help`. A malformed Envelope — a separator with no instruction behind it — is refused the same way.

An empty resolved scope is a successful no-op and is reported as such.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`gh` and `uv` on `PATH`. `gh` must be authenticated for read access to the current Project's repository.

**Skills**

The Manager must be Enabled so the dependency check can run.

**Capabilities**

The current Harness must be able to spawn subagents. Reviewing in the context that helped write the ticket is not a degraded mode; the Skill stops when this Capability is Unsatisfied.

## SEE ALSO

**/orchestrate --help**, **/kntnt select**
