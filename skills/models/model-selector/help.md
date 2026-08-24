# model-selector

## NAME

model-selector - compare configured AI model systems by price and performance

## SYNOPSIS

**/model-selector** [**recommend**] [*WORKLOAD*] [**--decision=route**|**--decision=renew**] [**--budget=**_AMOUNT_|**--quality=**_SCORE_] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **route** *PATH* [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** (**chart**|**compare**) *WORKLOAD* [**--decision=route**|**--decision=renew**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** [**show**|**add** (**model**|**channel**)|**edit** (**model**|**channel**) *ID*|**remove** (**model**|**channel**) *ID*|**history**|**reset**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **update** [**--force**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **observe** *PATH* **--artifact=**_PATH_ [**--** *INSTRUCTION*]

**/model-selector** **record** *PATH* [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--on** [**--harness=**_NAME_] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** (**--off**|**--status**) [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--review=**_IDENTITY_ (**--action=save**|**--action=failed**|**--action=ignore**) [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector` compares complete model systems rather than bare model families. A comparison point includes an exact model release or resolved alias, effort or thinking budget, serving mode, Harness, tools, policies, access channel, and effective commercial schedule.

First use creates a profile of the exact models and access channels available to the user. Channels may include subscriptions, direct metered APIs, gateway APIs, or other arrangements. The profile contains no credentials and is reused on later runs.

Recommendations are selected from comparable Pareto frontiers. Cash, rolling-window quota, weekly quota, subscription credits, allocated plan cost, latency, and quality remain separate unless the user supplies an explicit shadow price. Included subscription usage may have zero marginal cash cost while consuming scarce quota.

When representative matched measurements do not determine the exact point, cold start first chooses the weakest plausibly capable enabled model and then its lowest plausibly sufficient supported reasoning control. Reversible, objectively checked work begins there and escalates one adjacent reasoning rung only after verified failure. High-consequence or irreversible work without a trustworthy checker uses the strongest plausible enabled configuration and refuses unsafe exploration.

The bundled seed contains dated public model identities, categorical low-confidence first-party capability priors, direct and gateway prices, and benchmark priors. Capability prose can choose a cold-start experiment but never becomes a numeric score or a measurement-based recommendation. The seed contains no access profile, entitlement, account quota, or local evaluation. Every result reports evidence source, date, uncertainty, exclusions, and missing evidence.

## COMMANDS

**recommend** [*WORKLOAD*]

Choose one exact configuration and report its nearest cheaper and stronger comparable frontier neighbours. Bare `/model-selector` uses this command when the current workload is unambiguous.

**route** *PATH*

Resolve one versioned structured request or ordered batch into exact, Harness-native launch decisions and a reusable frozen snapshot without setup, network access, evaluation, or persistent writes.

**chart** *WORKLOAD*

Build the applicable frontiers without choosing one winner, then emit compact tables and plotting-ready CSV.

**compare** *WORKLOAD*

An alias of `chart`.

**setup**

Create the initial profile or perform a complete guided review of the existing profile.

**config**

Display or revise the model and access-channel profile. Its page lists every configuration subcommand.

**update**

Perform one bounded refresh of due model indexes, first-party capability sources, commercial terms, and benchmark releases. Changed capability claims append low-confidence prior records without rewriting history. Known immutable model detail pages and existing local run keys are not fetched or executed again.

**observe** *PATH*

Turn completed routed attempts into sanitized run observations in a caller-owned artifact. Only an external judgement establishes an outcome, unavailable measurements stay `null`, and nothing is imported until `record` is invoked explicitly.

**capture**

Opt in to automatic local run-evidence capture during ordinary Harness work, report its health, settle one deferred review, or turn it off again. Its page states what is installed, what is retained, and how long.

**record** *PATH*

Validate and append unseen local evaluation observations. Conflicting historical observations are preserved rather than overwritten.

**status**

Report the profile, evidence vintage, due sources, gaps, and provisional facts without network access or writes.

## OPTIONS

**--artifact=**_PATH_

Write the observations into the caller-owned artifact at *PATH*, creating it when absent and merging into it when present. Required by `observe` and valid with no other command.

**--data=**_PATH_

Use *PATH* as the profile and evidence directory. Valid with every command except `observe`, which reads neither. The default is `~/.model-selector/`.

**--decision=route**, **--decision=renew**

For `recommend`, `chart`, and `compare`, compare marginal routing economics now or whether a fixed subscription fee earns renewal. `route` is the default.

**--budget=**_AMOUNT_

For `recommend`, select the highest conservative quality within a budget when every eligible point uses a comparable cost unit. Mutually exclusive with `--quality`.

**--quality=**_SCORE_

For `recommend`, select the lowest conservative comparable cost that clears the quality floor. Mutually exclusive with `--budget`.

**--on**, **--off**

Consent to automatic capture and install its owned lifecycle integration, or stop it and remove every hook this feature owns. Valid only for `capture`. Accepted evidence survives `--off`, and making the Skill Disabled removes the same integrations without a second step.

**--status**

Report capture's own state: whether it is enabled, adapter health per Harness, pending-review count, oldest pending age, storage in use, and the retention bounds. Valid only for `capture`, and distinct from the `status` command, which reports the profile and the evidence.

**--review=**_IDENTITY_

Settle the pending capture named by *IDENTITY*. Valid only for `capture`, and requires `--action`.

**--action=save**, **--action=failed**, **--action=ignore**

Record a reviewed capture as a success, record it as a failure, or discard it. Valid only with `--review`, where explicit user confirmation is what makes the outcome evidence.

**--harness=**_NAME_

Install into the named Harness, repeatable; `claude-code`, `codex`, or `opencode`. Valid only with `--on`, and defaults to every supported Harness.

**--force**

For `update`, check every relevant mutable index once regardless of cadence. Known immutable details and existing observations remain untouched.

## OUTPUT

`recommend` opens with exactly one text-bearing evidence banner: `🔵 HEURISTISK STARTPUNKT` for an exploratory point chosen from workload heuristics and capability priors, `🟠 BLANDAD EVIDENS` when measurements exist but a decision-relevant heuristic assumption remains, or `🟢 MÄTDATABASERAD REKOMMENDATION` when representative matched measurements determine the exact point and its conservative quality clears the floor. The words carry the status; emoji color only reinforces it. Every banner states the classification reason, confidence, missing evidence, and whether the point is an exploration start or a production recommendation.

`route` emits structured `selected`, `inherit`, or `refused` decisions in request order. Only selection carries Harness-native launch arguments; every refusal carries a stable reason. Its returned snapshot freezes all routing inputs needed to reproduce later decisions.

The recommendation names the exact configuration, its decision rule, comparable neighbours, exclusions, uncertainty, and staleness. If the evidence cannot support the comparison, it identifies the missing evidence and proposes the smallest discriminating evaluation instead of inventing a rank.

After a blue or orange banner, `Snabbaste vägen till mätdata` gives an agent-ready sequential and parallel experiment brief with frozen task inputs, exact adjacent configurations, checker, measurements, run bound, stopping rule, and a `record`-compatible observation artifact. `recommend` plans the experiment but performs no network request, evaluation, or write; normal work executes the brief, and no separate experiment command exists.

`chart` and `compare` report separate cash, quota, and renewal views unless explicit shadow prices make a common numeric axis valid. Missing metrics are represented as `null`, never zero.

`update` records an outcome for every due source and reports each appended change. Discovering a newer model does not replace an Enabled version automatically; use `config add` or `config edit` to change membership.

## FILES

**~/.model-selector/config.json**

The default active profile and its revision history. A user-supplied `--data` directory relocates it.

**~/.model-selector/capture/**

The capture store while capture is enabled: its configuration, per-session drafts, and bounded pending-review records. An imported capture is deleted immediately; nothing here is permanent evidence.

**Evidence ledger**

An append-only, effective-dated record under the selected data directory. Configuration changes never delete it.

## DIAGNOSTICS

An incomplete form, unsupported combination, or option with no work to do is refused rather than ignored. The Skill names the error, prints the addressed command's SYNOPSIS, changes nothing, and points to that command's `--help` page.

No changed source is a successful `update`. Unreachable or insufficient evidence is reported without turning unavailable data into a zero or an invented comparison.

## EXAMPLES

**/model-selector recommend repository refactor --decision=route**

Select an exact configured system for a repository-refactoring workload using marginal routing economics.

**/model-selector route ./routing-request.json**

Resolve a caller-owned request artifact without changing profile or evidence state.

**/model-selector update --force**

Check every relevant mutable source once while retaining known immutable details and recorded observations.

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

`uv` runs the shipped offline routing module. Network access is used only by `update`; every other command operates on bundled or locally stored evidence and reports insufficiency.

## SEE ALSO

**/model-selector recommend --help**, **/model-selector config --help**, **/model-selector status --help**, **/kntnt select**
