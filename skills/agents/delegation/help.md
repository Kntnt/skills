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

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager and model-selector must be Enabled so the dependency check can run and delegated execution can be routed.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/delegation on --help**, **/delegation off --help**, **/delegation status --help**, **/brief --help**, **/kntnt select**
