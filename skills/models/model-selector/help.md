# model-selector

## NAME

model-selector - compare configured AI model systems by price and performance

## SYNOPSIS

**/model-selector** [**recommend**] [*WORKLOAD*] [**--decision=route**|**--decision=renew**] [**--budget=**_AMOUNT_|**--quality=**_SCORE_] [**--data=**_PATH_]

**/model-selector** (**chart**|**compare**) *WORKLOAD* [**--decision=route**|**--decision=renew**] [**--data=**_PATH_]

**/model-selector** **setup** [**--data=**_PATH_]

**/model-selector** **config** [**show**|**add** (**model**|**channel**)|**edit** (**model**|**channel**) *ID*|**remove** (**model**|**channel**) *ID*|**history**|**reset**] [**--data=**_PATH_]

**/model-selector** **update** [**--force**] [**--data=**_PATH_]

**/model-selector** **record** *PATH* [**--data=**_PATH_]

**/model-selector** **status** [**--data=**_PATH_]

## DESCRIPTION

`model-selector` compares complete model systems rather than bare model families. A comparison point includes an exact model release or resolved alias, effort or thinking budget, serving mode, Harness, tools, policies, access channel, and effective commercial schedule.

First use creates a profile of the exact models and access channels available to the user. Channels may include subscriptions, direct metered APIs, gateway APIs, or other arrangements. The profile contains no credentials and is reused on later runs.

Recommendations are selected from comparable Pareto frontiers. Cash, rolling-window quota, weekly quota, subscription credits, allocated plan cost, latency, and quality remain separate unless the user supplies an explicit shadow price. Included subscription usage may have zero marginal cash cost while consuming scarce quota.

When representative matched measurements do not determine the exact point, cold start first chooses the weakest plausibly capable enabled model and then its lowest plausibly sufficient supported reasoning control. Reversible, objectively checked work begins there and escalates one adjacent reasoning rung only after verified failure. High-consequence or irreversible work without a trustworthy checker uses the strongest plausible enabled configuration and refuses unsafe exploration.

The bundled seed contains dated public model identities, categorical low-confidence first-party capability priors, direct and gateway prices, and benchmark priors. Capability prose can choose a cold-start experiment but never becomes a numeric score or a measurement-based recommendation. The seed contains no access profile, entitlement, account quota, or local evaluation. Every result reports evidence source, date, uncertainty, exclusions, and missing evidence.

## COMMANDS

**recommend** [*WORKLOAD*]

Choose one exact configuration and report its nearest cheaper and stronger comparable frontier neighbours. Bare `/model-selector` uses this command when the current workload is unambiguous.

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

**record** *PATH*

Validate and append unseen local evaluation observations. Conflicting historical observations are preserved rather than overwritten.

**status**

Report the profile, evidence vintage, due sources, gaps, and provisional facts without network access or writes.

## OPTIONS

**--data=**_PATH_

Use *PATH* as the profile and evidence directory. Valid with every command. The default is `~/.model-selector/`.

**--decision=route**, **--decision=renew**

For `recommend`, `chart`, and `compare`, compare marginal routing economics now or whether a fixed subscription fee earns renewal. `route` is the default.

**--budget=**_AMOUNT_

For `recommend`, select the highest conservative quality within a budget when every eligible point uses a comparable cost unit. Mutually exclusive with `--quality`.

**--quality=**_SCORE_

For `recommend`, select the lowest conservative comparable cost that clears the quality floor. Mutually exclusive with `--budget`.

**--force**

For `update`, check every relevant mutable index once regardless of cadence. Known immutable details and existing observations remain untouched.

## OUTPUT

`recommend` opens with exactly one text-bearing evidence banner: `🔵 HEURISTISK STARTPUNKT` for an exploratory point chosen from workload heuristics and capability priors, `🟠 BLANDAD EVIDENS` when measurements exist but a decision-relevant heuristic assumption remains, or `🟢 MÄTDATABASERAD REKOMMENDATION` when representative matched measurements determine the exact point and its conservative quality clears the floor. The words carry the status; emoji color only reinforces it. Every banner states the classification reason, confidence, missing evidence, and whether the point is an exploration start or a production recommendation.

The recommendation names the exact configuration, its decision rule, comparable neighbours, exclusions, uncertainty, and staleness. If the evidence cannot support the comparison, it identifies the missing evidence and proposes the smallest discriminating evaluation instead of inventing a rank.

After a blue or orange banner, `Snabbaste vägen till mätdata` gives an agent-ready sequential and parallel experiment brief with frozen task inputs, exact adjacent configurations, checker, measurements, run bound, stopping rule, and a `record`-compatible observation artifact. `recommend` plans the experiment but performs no network request, evaluation, or write; normal work executes the brief, and no separate experiment command exists.

`chart` and `compare` report separate cash, quota, and renewal views unless explicit shadow prices make a common numeric axis valid. Missing metrics are represented as `null`, never zero.

`update` records an outcome for every due source and reports each appended change. Discovering a newer model does not replace an Enabled version automatically; use `config add` or `config edit` to change membership.

## FILES

**~/.model-selector/config.json**

The default active profile and its revision history. A user-supplied `--data` directory relocates it.

**Evidence ledger**

An append-only, effective-dated record under the selected data directory. Configuration changes never delete it.

## DIAGNOSTICS

An incomplete form, unsupported combination, or option with no work to do is refused rather than ignored. The Skill names the error, prints the addressed command's SYNOPSIS, changes nothing, and points to that command's `--help` page.

No changed source is a successful `update`. Unreachable or insufficient evidence is reported without turning unavailable data into a zero or an invented comparison.

## EXAMPLES

**/model-selector recommend repository refactor --decision=route**

Select an exact configured system for a repository-refactoring workload using marginal routing economics.

**/model-selector update --force**

Check every relevant mutable source once while retaining known immutable details and recorded observations.

## DEPENDENCIES

None. Network access is used only by `update`; every other command operates on bundled or locally stored evidence and reports insufficiency.

## SEE ALSO

**/model-selector recommend --help**, **/model-selector config --help**, **/model-selector status --help**, **/kntnt select**
