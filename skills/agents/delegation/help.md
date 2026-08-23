# delegation

## NAME

delegation - control delegation mode for a session, Project, or user

## SYNOPSIS

**/delegation** [**session**|**--session**]

**/delegation** [**session**|**project**|**user**|**--session**|**--project**|**--user**] (**on**|**off**|**--on**|**--off**) [**--yes**]

**/delegation** [**session**|**project**|**user**|**--session**|**--project**|**--user**] (**status**|**--status**)

## DESCRIPTION

`delegation` controls a mode in which the main agent plans, briefs, orchestrates, and verifies while subagents execute on the cheapest model the main agent judges able. It does not change the main agent's model or reasoning effort.

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

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Manager must be Enabled so the dependency check can run.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and does no work when it is unsatisfied.

## SEE ALSO

**/tldr --help**, **/kntnt select**
