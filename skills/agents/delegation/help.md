# delegation

## NAME

delegation - control delegation mode for a session, Project, or user

## SYNOPSIS

**/delegation** [**session**|**--session**] [**--** *INSTRUCTION*]

**/delegation** [**session**|**project**|**user**|**--session**|**--project**|**--user**] (**on**|**off**|**--on**|**--off**) [**--yes**] [**--** *INSTRUCTION*]

**/delegation** [**session**|**project**|**user**|**--session**|**--project**|**--user**] (**status**|**--status**) [**--** *INSTRUCTION*]

## DESCRIPTION

`delegation` controls a mode in which the main agent decides whether delegation is worthwhile, plans, briefs, orchestrates, and verifies while subagents execute. Once the main agent has chosen to delegate, it sends only that execution through model-selector's public `route` Interface. Routing never changes the main agent's model or deliberation configuration.

The separate decision whether predictably noisy tool work warrants delegation remains outside this routing mode.

With no arguments, it toggles the session scope. An explicit `on` or `off` changes the selected scope. `status` reports the selected scope, or all scopes when no scope is given. Scope and state may be written as bare words or equivalent long options, in either order.

The effective verdict is resolved in this order: an explicit session instruction wins; otherwise the mode is on when a managed block exists in a Project or user context file loaded by the current Harness. Project and user blocks contain identical instructions and therefore cannot create different mode definitions.

## SCOPES

**session**

Apply only to the current conversation. The state is also recorded in the Harness's per-session scratch directory when one exists, so context compaction does not silently lose it.

**project**

Write or remove a managed block in the context file this Project already loads. A committed block applies to everyone using the Project.

**user**

Write or remove the same managed block in this Harness's global context file. Run the Skill separately in another Harness to configure that Harness.

## STATES

**on**

Enable delegation mode in the selected scope.

**off**

Disable the selected scope. Session `off` suspends a standing Project or user block for the current conversation without removing its text; a later compaction may expose that block again.

**status**

Report scope state, the effective verdict, and any stale managed block without changing persistent state.

## OPTIONS

**--session**, **--project**, **--user**

Long-option aliases for the corresponding scope operands.

**--on**, **--off**, **--status**

Long-option aliases for the corresponding state operands.

**--yes**

Write or remove a persistent Project or user block without waiting for confirmation. It is valid only with `on` or `off`.

## FILES

**kntnt-delegation.json**

Optional state in the Harness's per-session scratch directory. It preserves session state across context compaction and does not outlive the session.

**Project and user context files**

The Skill shows the selected file and exact managed block before writing unless `--yes` is present. A block whose text differs from the current Skill is reported as stale; applying `on` rewrites it in place.

## DIAGNOSTICS

A persistent scope without a state, more than one scope or state, `status` combined with another state, and `--yes` without `on` or `off` are invalid. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/delegation --help`.

An option with no work to do is refused rather than ignored. In particular, `/delegation status --yes` is invalid.

## EXAMPLES

**/delegation**

Toggle delegation mode for the current session.

**/delegation project on**

Show and confirm a managed Project block that enables the mode for later sessions.

**/delegation status**

Report all scopes and the effective verdict.

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

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/tldr --help**, **/kntnt select**
