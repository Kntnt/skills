# delegation

## NAME

delegation - control delegation mode for a session, Project, or user

## SYNOPSIS

**/delegation** [**--** *INSTRUCTION*]

**/delegation** (**on**|**off**) [**--project**|**--user**] [**--yes**] [**--** *INSTRUCTION*]

**/delegation** **status** [**--project**|**--user**] [**--** *INSTRUCTION*]

## DESCRIPTION

Delegation mode leaves planning, delegation decisions, briefing, and verification with the main agent while subagents execute selected work. Model Selector routes delegated execution without changing the main agent's configuration; a spawn on the frozen main seat with no model, deliberation, or surface override is not routed.

No arguments toggles the current session. `on` and `off` change the selected scope; `status` reports one scope or all three.

The Skill takes no operand. The unnamed default is the session; **--project** and **--user** select persistent scopes. Only a bare `/delegation` toggles the session.

An explicit session setting wins over loaded Project and user blocks.

## COMMANDS

**on**

Enable delegation mode in the selected scope.

**off**

Disable delegation mode in the selected scope.

**status**

Report scope state, the effective verdict, and any stale managed files without changing persistent state.

## OPTIONS

**--project**

Target this Project's loaded context file and its two companion files instead of the current session. A committed trio applies to everyone using the Project.

**--user**

Target this Harness's global context file and its two companion files instead of the current session. Run the Skill separately in another Harness to configure that Harness.

**--yes**

Write or remove persistent Project or user files without waiting for confirmation. It is valid only with `on` or `off`.

## SCOPES

**session**

The default and the scope a bare invocation toggles. Session scratch preserves it across context compaction when available.

**project**

Selected by **--project**. A managed context pointer and two companion files can be committed for everyone using the Project.

**user**

Selected by **--user**. A managed pointer and two companions apply to the current Harness's global context.

## FILES

**kntnt-delegation.json**

Optional session scratch state used across context compaction.

**Project and user context files**

The Skill keeps a managed `@agents.d/kntnt-delegation.md` pointer and a read-when line for the fence in the loaded context file.

**agents.d/kntnt-delegation.md**

The companion contains the mode.

**agents.d/kntnt-delegation-fence.md**

The companion contains the canonical fence. The Skill shows all three managed files before writing unless **--yes** is present; `on` refreshes stale state.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the SYNOPSIS for the most specific page, changes nothing, and points to that page. A flag is refused rather than ignored where it has no work to do here.

**--yes** requires `on` or `off`; scope flags are mutually exclusive and require a command path. Unseparated text and a second command path are invalid.

Unseparated text is not an instruction.

## EXAMPLES

**/delegation**

Toggle delegation mode for the current session.

**/delegation on --project**

Show and confirm a managed Project pointer and two companions that enable the mode for later sessions.

**/delegation status**

Report all three scopes and the effective verdict.

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

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/delegation on --help**, **/delegation off --help**, **/delegation status --help**, **/brief --help**, **/kntnt select**
