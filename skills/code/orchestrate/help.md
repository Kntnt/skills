# orchestrate

## NAME

orchestrate - work ready-for-agent tickets in dependency waves

## SYNOPSIS

**/orchestrate** [*TICKET-OR-SPEC*...] [**--dry-run**] [**--at-once** *COUNT*] [**--model** *NAME*] [**--deliberation** *LEVEL*] [**--yes**] [**--** *INSTRUCTION*]

**/orchestrate reconcile** *TICKET* [**--commit** *COMMIT*] [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`orchestrate` plans and works the current repository's open `ready-for-agent` tickets on the branch where it starts. It claims each ticket, delegates the build to a fresh subagent, delegates verification to a different subagent, integrates verified work, records the outcome on the tracker, and closes successful tickets. It does not push, tag, or release.

Blocking relations produce dependency waves. Wave one contains tickets that can start immediately; each later wave contains work unblocked by earlier verified work. Native tracker dependency relations are authoritative when present. A ticket with no native relation may declare bare `#number` references on a `Blocked by` line. A closed blocker continues to block until it has a done Ticket Resolution.

The orchestrating session makes every plan, triage, integration, and verification judgement. Run it from the most capable model available; those judgements are only as reliable as that model. Before any claim, it sends the starting frontier as one ordered batch through model-selector's public route Interface and freezes the returned snapshot for the whole run. Every later frontier, replacement claim, amend, collision repair, rebuild, and mechanical wave fix is decided from that same frozen snapshot, in a request of its own, before it runs; nothing is claimed or dispatched that it has no acceptable decision for. Builders, amenders, collision repairers, rebuilders, and mechanical wave fixers launch with their selected exact Harness-native controls, or on the exact main seat where the decision reported inheritance. Every ticket, amend, repair, and wave verdict inherits the orchestrator's complete model and deliberation configuration exactly and is never routed at all; no builder override or route decision can affect it.

Before claiming anything, the Skill reads every ticket in scope for a decision the text leaves open and asks all such questions in one batch. Answers are posted to the corresponding ticket before building. With `--yes`, an open decision cannot be answered, so the ticket is parked under `needs-info` with its question and the rest of the scope continues.

`reconcile` is the explicit maintainer action for a ticket whose failed or conflicted unattended attempt was later completed outside Orchestrate. It preserves that Run Outcome, records a done Ticket Resolution naming the landed completion commit, and cleans stale workflow state without closing the already-closed ticket. See **/orchestrate reconcile --help**.

## COMMANDS

**reconcile**

Record that a closed, unsuccessfully attempted ticket was completed outside Orchestrate.

## POSITIONAL ARGUMENTS

*TICKET-OR-SPEC*...

Bare references such as `#14`. With no references, the scope is every open ticket carrying `ready-for-agent`. With references, the scope is the union of each named ticket and each named spec's children.

A reference filed as the parent of other tickets is a spec and is never built itself. Where the tracker exposes no parent relation, a `Parent` line in a ticket body is the fallback. A reference that does not resolve, is not a number, or uses `owner/repo#number` makes the complete invocation invalid.

Naming a ticket narrows the scope but does not bypass blockers, claims, readiness checks, or an outcome already recorded on the ticket.

## TICKET EXECUTION

**Claim**

The ticket is assigned before work starts. A ticket claimed by another user or another active run is skipped. An interrupted claim belonging to this run can be resumed when the tracker and branch support it.

**Build**

A fresh subagent receives the ticket body, its complete comment thread, the parent spec and its testing decisions, the Project's verification commands, the requirement to build test-first, and isolated scratch and reservation data. It receives no private summary of the ticket. The verification gate is resolved once at the run's start from the Project's contributing guide or configured checks; every verifier receives that exact list and neither substitutes nor expands it.

**Verify**

A different subagent receives the same ticket record but none of the builder's claims. It runs the Project's complete verification gate and checks every acceptance criterion. Delivery requests such as push, pull request, or release are reported but do not change the verdict because delivery is outside this Skill.

**Integrate**

Verified work is committed and integrated into the run branch. After each wave, the full Project gate runs on the combined branch and an independent coherence review checks cross-ticket facts that tests may not cover. Mechanical coherence findings are fixed by another subagent and checked again until a round is clean; a failed gate, an unresolved choice, or a fix that makes no progress stops the run.

**Close**

The ticket is closed only after its work is integrated and the combined branch passes. Its recorded outcome names the commit that carries the work.

## BUILDER STOPS

**Mechanical hinder**

A deterministic environment problem is repaired by the orchestrator and the same brief is attempted once more. If the hinder remains, it follows the failure path.

**Genuine decision**

An ambiguity, missing requirement, or design choice not settled by the ticket parks the ticket under `needs-info`, posts the question, releases the claim, and records no build outcome.

**Discovered dependency**

When the missing requirement is carried by another ticket without a done Ticket Resolution, the run writes the missing blocking edge to the tracker, releases the claim, discards the partial isolated build, and offers the ticket again after its blocker has a done Ticket Resolution. This does not consume the ticket's rebuild.

**Failed work**

A stop that is neither mechanical, a genuine decision, nor a discovered dependency enters the same verification-failure path as a failed build.

## FAILURES AND COLLISIONS

A verification failure receives amend 1. If its independent verifier also fails, that fresh complete verdict receives a second amend. Each attempt uses a fresh builder in the same ticket allocation and another fresh verifier with the ordinary full ticket brief; that verifier sees no earlier verdict or builder report. The path is bounded to at most two verifier-informed amends, and a failed final verdict after the second amend records the ticket failed with no third amend.

A merge collision is repaired on the ticket's own branch and verified against both tickets. If that repair fails, the ticket is rebuilt once from a clean base containing the work it collided with. A second collision records the ticket as conflicted.

With `--at-once 1`, unverified work is on the run branch, so an unrepaired failure stops later tickets. Above one, failures remain isolated and unrelated tickets continue; anything depending on failed work is stranded.

## CONTINUING A RUN

Restart an interrupted run with the same invocation and durable per-session state directory. There is no resume option. Recorded outcomes remain settled, and numbered amend markers preserve the exact builder, verifier, passed-verdict, or failed-verdict phase together with the latest complete verdict needed by a resumed builder. The frozen routing account is not reconstructed from current profile, evidence, price, alias, or Harness state: where it is absent while a claim of this run's remains, or where it cannot be read at all, the run stops rather than routing its remaining work from a context it never ran under. `--model` and `--deliberation` are part of that account, so a re-invocation that changes or drops either is refused rather than treated as a continuation. Repeating the same named attempt and phase resumes it without appending another event or spending the next attempt. A legacy unnumbered amend marker counts as attempt one.

A ticket still claimed by the current user is resumed only when the Skill can distinguish an interrupted claim from another active run. If the tracker cannot identify the current user, the Skill stops rather than guessing.

## OUTCOMES

Every ticket in scope appears once in the final report. Report groups tickets by their current Ticket Resolution while ticket detail retains the immutable Run Outcome and completion provenance that produced or later corrected it.

A recorded outcome and a current Ticket Resolution are different facts, wherever a ticket is read. The recorded outcome is the immutable record of one unattended attempt and never changes once written. The current Ticket Resolution is what the ticket's state is now: where no Reconciliation has been recorded, that state is the recorded outcome itself; where one has, the most recent Reconciliation states it instead, and the earlier outcome remains as unchanged history.

**done**

The requested work is complete. An ordinary successful run was built, independently verified, integrated, recorded, and closed by Orchestrate. A reconciled ticket was completed outside Orchestrate; its detail preserves the unsuccessful Run Outcome, Reconciliation provenance, and completion commit, and does not claim Orchestrate built or independently verified that repair.

**failed**

Verification did not pass. The ticket detail's `amends_spent` distinguishes an exhausted two-amend verification-repair path from work that failed before an available continuation amend completed. Work remains in the ticket's isolated working tree or, at a ceiling of one, on the run branch.

**conflicted**

Neither the collision repair nor the single rebuild produced an integrable result. The report names the colliding ticket and files.

**stranded**

Waiting directly or indirectly on a ticket that failed.

**never on the frontier**

Never became workable because of a cycle, an open blocker outside the run, another claim, a stopped integration, or a parked open decision.

The report also names the commit on which the run's work is based. A ticket recorded blocked on newly discovered work appears under the outcome implied by that open blocker rather than in a sixth category.

## OPTIONS

**--dry-run**

Read the tracker, resolve the requested scope, and report the dependency-wave graph and read-only routing readiness/proposed decisions without commenting on, parking, claiming, starting setup, or writing model-selector configuration, ledger, or run-state data.

**--at-once** *COUNT*

Build at most *COUNT* frontier tickets concurrently. The default is `1`. Values above one isolate each ticket in its own branch and working tree; `1` works directly on the current branch.

**--model** *NAME*

Lock only the building model dimension for every execution role. Model-selector still selects deliberation from the frozen snapshot. An unavailable, ambiguous, unmappable, or above-main exact model is refused before claims; it never falls through to another model. Verdicts retain exact main-seat inheritance.

**--deliberation** *LEVEL*

Lock only the building deliberation dimension for every execution role. *LEVEL* is exactly one of `low`, `medium`, `high`, `xhigh`, or `max`; another value is refused rather than normalized. Model-selector still selects model when it is omitted. Verdicts retain exact main-seat inheritance.

**--commit** *COMMIT*

Name the default-branch commit that completed a reconciled ticket. It applies only to `reconcile`; the action discovers the commit when one exact closing-reference candidate exists.

**--yes**

Assume yes for every yes-or-no question. A ticket containing an open choice is parked rather than guessed because the option cannot choose among alternatives.

## FILES

**.git/kntnt-orchestrate/**

Working trees, branches, reservations, and ticket scratch space used when concurrency requires isolation. Successful ticket resources are removed after integration. Failed and conflicted resources remain for inspection; abandoned repair and blocked partial builds are discarded.

**Per-session state directory**

Two records of one run. The claim account — claimed tickets, tracker login, planned frontier, and base commit — is remembered rather than relied on: the tracker and the branch reconstruct it, so losing it costs a tracker call. The frozen routing account — the snapshot every decision was made under, the invocation's model and deliberation locks, and every exact decision — has no second source, so the run refuses to plan, route, or claim without it rather than deciding remaining work from current profile, evidence, price, alias, or Harness state.

**Run-owned append files**

Builders leave proposed entries for files every ticket must append to, such as a changelog, in ticket-specific notes. The orchestrator applies those notes serially after each wave, and the combined branch verifies the entries with the rest of the work.

## DIAGNOSTICS

An invalid reference, option, option value, or option combination is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, starts nothing, and points to `/orchestrate --help`.

Routing is refused rather than adjusted. A response that is not this run's frozen snapshot, that changes that snapshot under its own identity, that is not the plan's starting frontier in plan order, that carries `--model` or `--deliberation` other than the ones the first frontier was routed under, or that decides a verdict role is rejected and nothing is frozen. A claim, amend, repair, rebuild, or wave fix whose exact role has no acceptable decision in that frozen account is refused before it runs. A route refusal is reported with its stable reason code and starts no work.

The working tree must contain no uncommitted non-ignored work when the run plans and immediately before a ticket closes. Commit or stash such work and restart. A repository with no ready ticket, no workable frontier, or only externally claimed work is reported without starting a build.

## EXAMPLES

**/orchestrate --dry-run**

Print the dependency-wave plan and proposed read-only routing decisions for every open `ready-for-agent` ticket without claiming one.

**/orchestrate #14 #21 --at-once 2 --deliberation high**

Work the union of two ticket or spec references with at most two concurrent builders.

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

`git`, `gh`, and `uv` on `PATH`. `gh` must be authenticated with write access to the current repository and support issue dependencies and sub-issues.

**Skills**

The Manager and Model Selector Skills must be Enabled so the dependency check can run and Orchestrate can use model-selector's public route Interface.

**Capabilities**

The current Harness must be able to spawn subagents. The Skill asks the Harness to confirm this capability and starts nothing when it is Unsatisfied.

## SEE ALSO

**/ready-for-agent-check --help**, **/commit --help**, **/release --help**
