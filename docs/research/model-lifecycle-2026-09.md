# Model Selector: automatic model lifecycle

Researched on **2026-09-11**, against `main` at `1895c21b3fc993ddc5faf2fff306de21d4f2ddf2`, on the maintainer's Mac. This is a findings document, not a change to the current rules. No GitHub issues were filed. Issues #303–#307 were read for overlap and remain outside this investigation.

## Verdict

**A portable unattended daily pass is feasible, and `/model-selector update` can cease to be a routine maintenance requirement.** All three installed harnesses have headless execution. Claude and Codex also expose model discovery without inference through their control protocols; OpenCode has a catalogue-list command, and its configured OpenRouter gateway has an authenticated model-list endpoint. Portability does not need to be dropped.

This is **not achievable merely by scheduling today's Update instructions**. Adoption cannot remove a model; missing models can return errors that also mean lost access; new catalogue entries remain disabled by the current profile; and OpenCode's current planned launch does not reach the installed CLI. A lifecycle controller must handle these distinctions, stage the agent's reading, retain the last good facts when evidence is ambiguous, and publish the changes it applies.

Take the maintainer's premise as given: a released version at a particular deliberation does not change behavior over time. **No measurement ageing, decay, expiry, periodic rebenchmarking, or transfer of measurements to a successor is proposed.** Availability and prices are changing world facts; measurements of a version are historical evidence. Resolve moving aliases to version identities before associating either.

## Evidence conventions and local scope

- **Local** means a command actually run on this machine, or the named source symbols read at the commit above. Command output below is exact where quoted; projections explicitly omit unrelated fields. `$S` means the investigation's temporary directory, `/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/model-lifecycle-6qbp2ds5`. It was removed after verification. `$HERE` means the repository's `skills/models/model-selector` directory.
- **Documentation** links name first-party documentation or versioned first-party source. These establish the documented interface, not a successful live generation on this account.
- **Proposal** identifies policy choices inferred from the findings. No provider promises that a chosen retry count establishes retirement.
- Probe subprocesses ran from `$S/work`, with their own process groups and outer deadlines. Codex used a temporary `CODEX_HOME`, populated only with a private copy of its existing authentication file; OpenCode used temporary XDG data/cache/state directories and a private copy of its existing authentication file. Claude used `--safe-mode` and `--no-session-persistence` to suppress ambient hooks and session persistence while retaining subscription authentication. Temporary authentication copies were deleted.
- No valid-model inference probe, real adoption, definition regeneration, or scheduled-job installation was performed. Bogus IDs were used once each. OpenRouter received metadata GETs only from the investigation's HTTP client; no completion POST was made by that client.

Local baseline:

```text
$ git branch --show-current
main
$ git rev-parse HEAD
1895c21b3fc993ddc5faf2fff306de21d4f2ddf2
$ claude --version
2.1.268 (Claude Code)
$ codex --version
codex-cli 0.154.0
$ opencode --version
1.18.29
```

Read-only inspection of `~/.kntnt/model-selector/profile.json` found Claude Max 20x through Claude Code, ChatGPT Pro 20x through Codex, and the `spacexai` API channel through OpenCode/OpenRouter. Its explicit model allowlist is:

```text
claude-fable-5-1
claude-opus-5
claude-sonnet-5
gpt-6-astra
gpt-5.6-sol
gpt-5.6-luna
grok-4.6
```

`catalogue.load`, `profiles.load` and `launch.definitions` were called read-only with Python bytecode writing disabled. The merged catalogue has **9 models and 22 plans**, the profile enables **7 models**, and the requested generated matrix has **15 definitions**. The refreshed file alone contains only OpenAI plans; the other providers' plans remain from the seed. This distinction matters when discovering changes.

## 1. Can each CLI list models this account can use?

### Claude Code

**There is no ordinary documented `claude models --json` command. There is a non-generative programmatic list.** Interactive `/model` presents the account's picker. The supported Agent SDK provides `query.supportedModels()` and `query.initializationResult()`, whose result includes models. [Claude account model picker](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code), [Agent SDK TypeScript reference](https://code.claude.com/docs/en/agent-sdk/typescript).

Local evidence: started this exact CLI argv, sent the following newline-delimited JSON request on stdin, read the matching response, and terminated the process group. No user prompt or inference request was sent:

```sh
claude -p --input-format stream-json --output-format stream-json --verbose \
  --safe-mode --no-session-persistence --tools '' \
  --permission-mode dontAsk --permission-prompts none
```

```json
{"type":"control_request","request_id":"lifecycle-init","request":{"subtype":"initialize"}}
```

It returned `type: control_response`, `response.subtype: success`, with `response.response.models`. Exact projection of each entry's `value`, `resolvedModel`, and supported levels:

| `value` | `resolvedModel` | `supportedEffortLevels` |
|---|---|---|
| `default` | `claude-opus-5[1m]` | low, medium, high, xhigh, max |
| `opus[1m]` | `claude-opus-5[1m]` | low, medium, high, xhigh, max |
| `fable` | `claude-fable-5-1` | low, medium, high, xhigh, max |
| `sonnet` | `claude-sonnet-5` | low, medium, high, xhigh, max |
| `haiku` | `claude-haiku-4-5-20251001` | field absent |

The same response identified `subscriptionType: Claude Max` and `apiProvider: firstParty`. This is useful account-context discovery, including alias resolution; `[1m]` is a serving selector, not a different measured release.

**Network/auth/cost:** subscription authentication was present. No model tokens were generated, and no metadata-list fee was found in the documentation. This run did not measure initialization's individual network requests or test it offline/unauthenticated. Therefore do not call the list an independently verified, exhaustive entitlement API, or treat omission of an older full model ID as retirement. Prefer the documented SDK method over depending on the raw control protocol without a version compatibility test.

The separate `GET https://api.anthropic.com/v1/models` requires an API key and `anthropic-version: 2023-06-01`; its paginated result has `data`, `first_id`, `last_id`, and `has_more`. It is an API-channel list, not proof of subscription access. No API key was obtained or used for it here. [Anthropic List Models](https://platform.claude.com/docs/en/api/models/list).

**Uncertain:** completeness beyond picker choices, offline freshness, access filtering under other plans/providers, and future raw-control compatibility. None prevents using this as positive discovery with conservative absence handling.

### Codex CLI

**No top-level `codex models` command appears in installed help, but `codex app-server` exposes the documented `model/list` JSON-RPC method.** It supplies model IDs, reasoning options and hidden/default markers. [Codex App Server](https://learn.chatgpt.com/docs/app-server#list-models-modellist).

Local exact command and request sequence, with each response read before the next request:

```sh
codex app-server --listen stdio://
```

```json
{"id":0,"method":"initialize","params":{"clientInfo":{"name":"model_lifecycle_research","version":"0.1"},"capabilities":{}}}
{"method":"initialized","params":{}}
{"id":1,"method":"model/list","params":{"limit":100,"includeHidden":true}}
```

Exact projection of the response's `result.data`:

| `model` | `hidden` | `defaultReasoningEffort` |
|---|---|---|
| `gpt-6-astra` | false | medium |
| `gpt-reserve` | true | medium |
| `gpt-5.6-sol` | false | low |
| `gpt-5.6-terra` | false | medium |
| `gpt-5.6-luna` | false | medium |
| `gpt-5.5` | false | medium |
| `gpt-5.3-codex-spark` | false | high |
| `codex-auto-review` | true | medium |

`nextCursor` was `null`. Astra, Sol and Terra advertised low/medium/high/xhigh/max/ultra; Luna and the hidden models low through max; 5.5 and Spark low through xhigh. Hidden/internal models are not automatic enrollment candidates. A launcher must implement the intersection of the model's controls, the installed CLI's controls and Model Selector's vocabulary; `ultra` is outside the current vocabulary.

**Network/auth/cost:** existing ChatGPT authentication was copied into the temporary home; no cached models file was copied. After the exchange, the newly created cache carried:

```json
{"fetched_at":"2026-09-11T09:36:30.639302Z","etag":"W/\"c74abdec3380c0b081c8c239cf3dfe6b\"","client_version":"0.154.0"}
```

No thread or turn was started by this listing exchange, so there was no inference-token use. No model-list fee was found. A current remote catalogue requires network/auth; a returned list must not be assumed fresh just because the RPC succeeds. Read all pages, include hidden entries when checking disappearance, and distinguish discovery from live availability.

Matching-version source makes the freshness limitation concrete: `supported_models` calls `OnlineIfUncached`; the manager has a **300-second cache TTL**, starts with bundled models, and returns its current models even when a refresh fails. A fresh temporary home eliminates an old cache, **not bundled fallback**. A successful ChatGPT catalogue with visible entries replaces the bundled list; other cases can merge with it. Save refresh diagnostics and cache freshness, and require independent corroboration for disappearance. [Codex 0.154.0 model-list adapter](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/app-server/src/models.rs), [model manager](https://github.com/openai/codex/blob/rust-v0.154.0/codex-rs/models-manager/src/manager.rs).

The public OpenAI API's `GET /v1/models` is a different authentication/channel surface and supplies no prices. It must not be substituted for the ChatGPT subscription list. [OpenAI Models API](https://developers.openai.com/api/reference/python/resources/models/methods/list).

**Uncertain:** exhaustive subscription entitlement guarantees and behavior of other CLI versions. The local exchange proves discovery works here, not that list omission proves a model was globally retired.

### OpenCode and its OpenRouter channel

**The list command exists, but lists the client's configured catalogue, not tested entitlements.** Exact installed form:

```sh
opencode models openrouter --pure --refresh
# Optional metadata form, documented/help-verified but not executed here:
opencode models openrouter --verbose
```

Local first command exited **0**, wrote `Models cache refreshed` to stderr, and printed **361 newline-separated IDs**. Exact output subset selected by `/x-ai/`:

```text
openrouter/x-ai/grok-4.20
openrouter/x-ai/grok-4.20-multi-agent
openrouter/x-ai/grok-4.3
openrouter/x-ai/grok-4.5
openrouter/x-ai/grok-4.6
openrouter/x-ai/grok-build-0.1
```

`--verbose` prints each ID followed by an indented JSON metadata object. `--refresh` refreshes **models.dev**, not OpenRouter account entitlements. Versioned source loads models.dev plus configuration, enables providers when credentials/configuration are present, and removes deprecated/blacklisted entries. [OpenCode CLI](https://opencode.ai/docs/cli/), [v1.18.29 models command](https://github.com/anomalyco/opencode/blob/v1.18.29/packages/opencode/src/cli/cmd/models.ts), [v1.18.29 provider implementation](https://github.com/anomalyco/opencode/blob/v1.18.29/packages/opencode/src/provider/provider.ts).

There is a better structured source for **this account's configured gateway**:

```http
GET https://openrouter.ai/api/v1/models/user
Authorization: Bearer <the existing OpenRouter API key>
```

The investigation executed this with Python `urllib.request.Request(url, headers={"Authorization": "Bearer " + key})`, then `urllib.request.urlopen(..., timeout=20)`, keeping the key in memory and out of output. It also fetched public `GET /api/v1/models` without auth. Exact output projection:

```text
models HTTP 200 count 439
models/user HTTP 200 count 426
```

Both included `x-ai/grok-4.6`, `expiration_date: null`, and these identical fields:

```json
{
  "pricing": {
    "prompt": "0.000002", "completion": "0.000006",
    "web_search": "0.005", "input_cache_read": "0.0000005",
    "overrides": [{"min_prompt_tokens":200000,"prompt":"0.000004",
      "completion":"0.000012","input_cache_read":"0.000001"}]
  },
  "reasoning": {"mandatory":true,"default_enabled":true,
    "supported_efforts":["xhigh","high","medium","low"],"default_effort":"high"}
}
```

The user endpoint filters provider preferences, privacy settings, guardrails and relevant routing constraints. With no offset/limit it documents returning the full list; a paginated client must follow the endpoint's pagination contract. It does **not** promise sufficient credit or healthy live endpoints. [OpenRouter user-filtered models](https://openrouter.ai/docs/api/api-reference/models/list-models-filtered-by-user-provider-preferences-privacy-settings-and-guardrails).

**Network/auth/cost:** `--refresh` needs network; cached client listing need not refresh the network feed. Provider credentials affect which providers are configured. `/models/user` needs network and bearer auth; public `/models` needs network but no auth. None generates tokens; no metadata-GET fee is documented. OpenRouter prices belong to its gateway, not automatically to Anthropic/OpenAI direct channels.

**Uncertain:** account credit and runtime endpoint availability, provider-specific lists outside OpenRouter, and why all individual entries differ between the 361/426/439 sets. Their observed difference alone rules out treating these lists as interchangeable retirement evidence.

## 2. Minimal probes and failure signatures

### What the current planner actually produces

Local evidence: imported `catalogue`, `profiles`, `launch` with `sys.dont_write_bytecode=True`, loaded the real files read-only, and called `launch.plan(model, 'low', 'process', profile, cat, repo='/tmp/lifecycle', read_only=True)`. The three command shapes were:

```sh
claude -p --add-dir /tmp/lifecycle --tools '' --model claude-sonnet-5 --effort low
codex exec -C /tmp/lifecycle --skip-git-repo-check -m gpt-5.6-luna \
  -c model_reasoning_effort=low -s read-only --json
opencode run --cwd /tmp/lifecycle --model spacexai/grok-4.6
```

For probes, only the requested model ID was made bogus, the working directory was scratch, and output/isolation/permission controls were added. No fallback model was enabled. Calling a fallback would test another model and invalidate the availability conclusion.

### Actual bogus-model results

**Claude:** exact executed command, 30-second outer deadline:

```sh
claude -p --add-dir "$S/work" --tools '' --safe-mode \
  --no-session-persistence --permission-mode dontAsk --permission-prompts none \
  --output-format json --max-budget-usd 0.01 \
  --model claude-kntnt-nonexistent-20260911 --effort low 'Reply only OK.'
```

Exit **1**, **1.69 seconds** including startup/registration. Exact result-field projection:

```json
{
  "type":"result", "subtype":"success", "is_error":true,
  "terminal_reason":"api_error", "api_error_status":404,
  "duration_api_ms":0, "total_cost_usd":0,
  "result":"There's an issue with the selected model (claude-kntnt-nonexistent-20260911). It may not exist or you may not have access to it. Run --model to pick a different model."
}
```

All input/output/cache counters were zero. Stderr:

```text
[claude-code:unrecognized_model] {"model":"claude-kntnt-nonexistent-20260911","query_source":"sdk"}
```

**Classify this as unavailable-or-unknown, not unambiguous global retirement.** `subtype: success` alone is specifically unsafe: `is_error`, terminal reason and status contradict successful inference. The SDK's `model_not_found` likewise includes account/deployment unavailability. [Claude SDK error types](https://code.claude.com/docs/en/agent-sdk/typescript).

**Codex:** exact executed command, 30-second outer deadline:

```sh
codex exec -C "$S/work" --skip-git-repo-check \
  -m gpt-kntnt-nonexistent-20260911 -c model_reasoning_effort=low \
  -s read-only --json --ephemeral --ignore-user-config \
  -c 'approval_policy="never"' -c features.shell_tool=false 'Reply only OK.'
```

Exit **1**, **2.63 seconds**. A preliminary `item.completed` error said:

```text
Model metadata for `gpt-kntnt-nonexistent-20260911` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

That is a **metadata warning**, not proof of a failed model request. The subsequent `error` and `turn.failed` events embedded this server error JSON in their message strings:

```json
{"type":"error","status":400,"error":{"type":"invalid_request_error","message":"The 'gpt-kntnt-nonexistent-20260911' model is not supported when using Codex with a ChatGPT account."}}
```

This establishes unsupported-on-this-channel, not retired worldwide. No assistant answer or usage event was produced. The subscription was used; no incremental API charge was demonstrated, but the CLI supplied no authoritative dollar total for this failure.

**OpenCode, actual planned shape:**

```sh
opencode run --cwd "$S/work" --model spacexai/kntnt-nonexistent-20260911 \
  --pure 'Reply only OK.'
```

Exit **1**, **0.27 seconds**, empty stdout, command usage on stderr. Installed help lists `--dir`, not `--cwd`. This is a local command failure, before model availability can be established. Independently, `_opencode` uses `model.provider/model.id`; the real configured route is `openrouter/x-ai/grok-4.6`, not `spacexai/grok-4.6`, and `_opencode` never reads the profile's `gateway`.

One additional diagnostic used the corrected CLI/provider shape with a **different bogus ID**, to see the installed error envelope; it is explicitly not claimed as a successful test of today's planner:

```sh
opencode run --dir "$S/work" --model openrouter/x-ai/kntnt-no-such-model-20260911 \
  --pure --format json 'Reply only OK.'
```

Exit **1**, **0.71 seconds**, empty stderr. Exact error payload, excluding event time/session ID:

```json
{"name":"UnknownError","data":{"message":"Unexpected server error. Check server logs for details.","ref":"err_3eeecd03"}}
```

The scratch OpenCode log was empty. **Do not invent a provider “not found” result behind that wrapper.** Versioned `Provider.getModel` source can throw `ProviderModelNotFoundError` for either a missing local provider or local model; the same class can arise from missing credentials/configuration or stale metadata. Even that more specific class would not establish retirement. [OpenCode v1.18.29 provider source](https://github.com/anomalyco/opencode/blob/v1.18.29/packages/opencode/src/provider/provider.ts). Session error conversion has a generic `Error` to `Unknown` branch, but the precise loss of this diagnostic's inner message remains unexplained. [Session error conversion](https://github.com/anomalyco/opencode/blob/v1.18.29/packages/opencode/src/session/message-v2.ts).

A separate **metadata lookup**, not a generation probe, did establish an unambiguous absence in OpenRouter's model namespace:

```text
GET https://openrouter.ai/api/v1/model/x-ai/kntnt-no-such-model-20260911
HTTP 404
{"error":{"message":"Model not found: x-ai/kntnt-no-such-model-20260911","code":404}}
```

Executed with unauthenticated `urllib.request.urlopen(url, timeout=15)`; the exception's HTTP code and response body were printed. The documented singular `/model/{author}/{slug}` endpoint resolves aliases and returns 404 for nonexistent models/aliases. This is stronger gateway-namespace evidence than “no endpoints,” but still does not establish retirement at the original provider. [OpenRouter models overview](https://openrouter.ai/docs/guides/overview/models).

### Separate failures before counting absence

| Evidence | Classification; effect on retirement counter |
|---|---|
| CLI usage/unknown flag, local missing provider/model, metadata-fallback warning, malformed events | Adapter/configuration/metadata failure; never increment |
| Explicit model missing **or access denied**, unsupported ChatGPT model | Account/channel unavailable or ambiguous; never increment global retirement |
| 401/authentication failure; 403/permission or policy denial | Auth/access failure; never increment |
| 402/billing/insufficient credit; 429/rate limit or exhausted allowance; spend-limit message even if HTTP 400 | Billing/quota failure; never increment |
| 5xx, overload, unavailable provider, “no endpoints,” connection/DNS/TLS failure | Outage/routing failure; never increment |
| Outer process deadline, provider timeout, interrupted stream | Timeout/unknown; never increment |
| Successful, complete metadata lookup explicitly says this exact model does not exist; or verified effective retirement notice | Qualifying absence in the namespace/channel the source actually governs |

These categories are documented for [Anthropic API errors](https://platform.claude.com/docs/en/api/errors) and [OpenRouter errors](https://openrouter.ai/docs/api_reference/errors-and-debugging). Anthropic documents 401 `authentication_error`, 402 `billing_error`, 403 `permission_error`, 404 `not_found_error`, 429 `rate_limit_error`, 500 `api_error`, 504 `timeout_error`, 529 `overloaded_error`; spend limits may also use 400. HTTP 200 does not establish successful streaming completion. Codex's actual subscription 400 above is local evidence; do not assume direct API error spellings always survive its event wrapper. Unknown future signatures remain unknown.

### Cost and probe policy

The actual Claude bogus probe reported **$0 and zero tokens**. The Codex bogus request produced no completion/usage event. The planned OpenCode call failed argument parsing; the corrected call returned a local/generic error with no completion. No successful OpenRouter generation occurred and no model-generation charge was observed; there is no gateway invoice measurement for the generic OpenCode error. The metadata GETs make no inference requests and have no documented token charge. The investigation did not spend a valid-model OpenRouter call to resolve uncertainty.

A valid probe has **no fixed universal price**: the CLI adds system/tool context, a reasoning model may generate hidden tokens, and title generation or other background work may add calls. For a single response, estimate `sum(tokens_in_category × applicable_USD_per_MTok / 1e6)`, including cache/reasoning and context tiers. For illustration only, 1,000 uncached input and 8 output tokens at the observed Grok gateway base price cost **$0.002048**; that is not an observed OpenCode probe bill or a bound on its actual context. The user's saved gateway override is a different card (input 0.9915/output 6.174 per MTok), another reason not to assert a fixed cash price from catalogue data.

**Proposal:** list first; use at most one small probe per candidate per daily pass only when metadata cannot settle channel availability. Select the lowest actually launchable deliberation, disable tools/fallbacks and ancillary calls where supported, record the actual served identity, and impose a deadline. Availability probes must not become success/failure measurements. No retries against the same model inside the pass. A controller cannot promise a few-cent cap merely by prompting “reply OK”; paid probing requires a real provider/key limit or a verified per-request token/context bound.

**Uncertain:** no genuinely retired real model was called; account-auth/quota/outage failures were not deliberately induced. Therefore the evidence does not provide an exclusive retired-model inference signature for any of the three current subscription/client launch paths. It provides a reason **not to use their ambiguous failures as such a signature**.

## 3. Can a detached pass do today's web reading and adoption?

**Yes as a controller plus a headless researcher.** The researcher can fetch/read pages and return a staged JSON bundle. The controller can then invoke `catalogue.py adopt` and `setup_apply.py`. No interactive session is intrinsically necessary; credentials, usable web access, tool permissions and bounded execution are necessary. This end-to-end write path was not exercised against the live store because the investigation expressly forbids it.

### What grade.py already proves, and what it does not

Local source evidence: `grade.dispatch` starts `uv run <grade.py> --once --data=<data>` using `subprocess.Popen`, `stdin/stdout/stderr=DEVNULL`, `cwd=_safe_home()` and `start_new_session=True`. `hook_pass` does local free grading and dispatches only when pending work exists. A lock prevents concurrent passes. `_bridge` obtains an argv from `selection.py --harness=process --read-only`, and `_judge_for` invokes that argv with a prompt.

The installed constants are **20 calls/pass**, **30 seconds per judge subprocess**, **20 seconds for each selection subprocess**, a **50 judged-row rolling-day check**, and **900 seconds stale-lock age**. These are not a dollar cap or a whole-pass deadline. The daily check is made before the loop against successful judged rows, not prepaid request expenditure; failed attempts can still cost money. Selection plus call time across 20 attempts can exceed 900 seconds. `subprocess.run(timeout=...)` is not a demonstrated all-descendant process-tree kill policy. Reuse the detached execution idea, not a claim that this is already a daily, strictly cost-bounded lifecycle scheduler.

The investigation's own detached control/probe processes used `Popen(..., start_new_session=True)` and an outer monotonic deadline, followed by process-group SIGTERM and SIGKILL if necessary. They ran without a terminal. That locally demonstrates the process architecture, not a completed autonomous price refresh.

### Exact forms and required permissions

The following are **implementation examples, not runs performed here**. `$MODEL` must be a discovered, approved researcher model; `$BRIEF` is a self-contained bounded reading instruction, carrying known facts/source URLs and asking for a complete staged JSON result with per-field evidence. It must not rely on an interactive Skill invocation being auto-loaded. The parent saves the final JSON and calls the scripts itself.

**Claude Code, subscription-compatible:**

```sh
claude -p "$BRIEF" --model "$MODEL" --effort low --safe-mode \
  --no-session-persistence --output-format json \
  --tools 'WebFetch,WebSearch' --allowedTools 'WebFetch,WebSearch' \
  --permission-mode dontAsk --permission-prompts none \
  --max-turns 12 --max-budget-usd 0.50
```

`--tools` controls exposure, `--allowedTools` preauthorizes use, and unresolved permissions are denied. Give it catalogue/source context in the prompt and save its final output from the parent; it needs no live-state write access. `--max-turns` is documented, though not displayed in this version's help; verify acceptance when implementing. `--max-budget-usd` is based on estimated usage and can only stop after incurred work; it is not an authoritative billing guarantee. Do **not** replace `--safe-mode` with `--bare` for the maintainer's Max subscription: current `--bare` ignores OAuth/keychain and requires API authentication. [Claude CLI reference](https://code.claude.com/docs/en/cli-reference), [headless execution](https://code.claude.com/docs/en/headless), [cost accounting](https://code.claude.com/docs/en/costs).

Direct in-agent adoption would additionally need `Bash` and an exact script-command allow rule. Regenerating `~/.claude/agents` is less straightforward: `.claude` is a protected path, and `dontAsk` denies protected writes that still require approval. This is not a reason to discard portability; a trusted non-agent controller can perform the authorized deterministic adoption/sync. Do not grant global permission bypass merely to make the researcher able to edit that directory. [Claude permission modes](https://code.claude.com/docs/en/permission-modes).

**Codex:**

```sh
codex exec -C "$S/work" --skip-git-repo-check --ephemeral \
  --ignore-user-config --ignore-rules -m "$MODEL" \
  -c 'model_reasoning_effort="low"' -c 'approval_policy="never"' \
  -c 'web_search="live"' -c features.shell_tool=false \
  -s read-only --json -o "$S/research-result.txt" "$BRIEF"
```

Use an isolated automation configuration/home with existing authorized authentication, rather than accidentally inheriting hooks, MCP servers, plugins or project instructions. `web_search="live"` allows live retrieval; cached search is insufficient to certify a fresh price. Installed top-level `--search` also exists, but config overrides are accepted directly by `exec`. An external fetch command would need shell-tool access and sandbox network permission; native web retrieval does not require granting arbitrary shell network. [Codex noninteractive mode](https://learn.chatgpt.com/docs/non-interactive-mode), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Direct in-agent adoption would need the shell tool enabled, `workspace-write`, and the specific data and definitions directories granted with `--add-dir`. `approval_policy="never"` prevents a hanging approval, but does not itself grant permissions. A restricted researcher plus parent adoption needs none of that broader write access. No stable general-purpose `codex exec --max-budget-usd`/`--max-turns` interface was found in local help. The documented rollout token-budget feature is under development; do not sell it as a verified hard dollar cap.

**OpenCode:**

```sh
opencode run --dir "$S/work" --model "$MODEL" --variant low \
  --pure --format json "$BRIEF"
```

Here `$MODEL` is a provider-qualified launch ID such as `openrouter/x-ai/grok-4.6`, not the catalogue's provider spelling. Use an isolated config, with `OPENCODE_PERMISSION` set to `{"*":"deny","webfetch":"allow"}` for a reader supplied with known URLs; add an appropriately configured `websearch` only if discovery needs it. Configure a dedicated primary agent with `steps: 12`; supply it with `--agent <name>` if not the configured default. Return the JSON in its final text and let the parent save it. Native page fetching suffices for the known-source reading; it still costs model tokens to interpret the text. [OpenCode permissions](https://opencode.ai/docs/permissions/), [agent step limit](https://opencode.ai/docs/agents/#max-steps).

Versioned `run.ts` rejects permission requests by default in noninteractive mode; `--auto` approves requests not explicitly denied. An explicit allowlist is sufficient and avoids broad auto-approval. Direct in-agent script execution would need exact `bash` permissions and `external_directory` permissions for paths outside the workspace. Steps limit iterations, not token billing, retries or elapsed time. No dollar-budget CLI flag was found. [OpenCode v1.18.29 run implementation](https://github.com/anomalyco/opencode/blob/v1.18.29/packages/opencode/src/cli/cmd/run.ts).

In each case the **parent's final deterministic sequence**, after checking the staged document and recording its proposed diff, is:

```sh
uv run "$HERE/scripts/catalogue.py" adopt "$S/facts.json" --data="$DATA"
uv run "$HERE/scripts/setup_apply.py" --data="$DATA"
```

That sequence is existing interface syntax. Lifecycle retirement and the stronger transaction/journal described below still need implementation; no such code is claimed to exist today.

### Daily scheduling and real bounds

**Proposal:** one shared Python controller and three small harness adapters. Use one account-wide lock and a persisted daily attempt marker, with a resumable due-source list. At most one researcher process at a time; no nested lifecycle/grading hooks. Reserve budget before launching a call, charge failures too, cap fetched body sizes and source count, and persist elapsed time, observed usage/cost, timeout/cap reasons and the next due time. Read unchanged-source hashes to avoid paying for another interpretation; discovery must still examine provider model indexes/release feeds, not only URLs of already-known models.

Set a concrete initial **300-second whole-pass deadline**, including discovery, research and application, with **30-second individual discovery/probe deadlines**, process-group termination and a brief forced-kill grace. A cap leaves the last accepted catalogue intact and reports deferred work. These numbers are proposed defaults, not measured throughput guarantees. Long source lists may need successive daily passes; report the oldest unverified source instead of stamping all facts current.

For money, distinguish a **$0.50 daily target** for agent reading from enforcement. Claude has an estimated-dollar stop; Codex and OpenCode do not expose an equivalent verified hard CLI limit. Bound their loop/output as supported and monitor usage, allowing for in-flight overshoot. When a strict API-dollar ceiling is required, use a dedicated provider-enforced budget/key, conservatively reserve maximum request costs, or leave that paid adapter unavailable until such enforcement exists. OpenRouter documents keys with dollar limits and daily/weekly/monthly resets; no key was created or changed here. A process timeout alone cannot recall already submitted billable work. Subscriptions consume allowance rather than a fixed incremental API bill; authentication/quota failures must be visible. [OpenRouter key creation and limits](https://openrouter.ai/docs/api/api-reference/api-keys/create-a-new-api-key).

A session-end trigger with a 24-hour due check is **not daily execution on an idle machine**. For this Mac, use an owned user `launchd` job with `StartCalendarInterval` and a due check on startup/wake. Local command `man launchd.plist | col -b` describes calendar scheduling and coalescing missed sleep intervals into one wake event; `StartInterval` can miss sleep firings. The scheduling layer is independent of the chosen harness. Other operating systems need their own scheduler adapter; nothing about Claude/Codex/OpenCode requires a particular scheduler. No scheduler runs while the machine is powered off, or obtains new credentials by itself.

**Uncertain:** the full source-reading/adoption workflow has not been acceptance-tested in each sandbox; web blocking, managed policy, expired subscription credentials and CLI version changes remain operational failures to report. A universal hard financial cap is not established by the three CLI interfaces. These are testable adapter/budget requirements, not evidence that harness portability is impossible.

## 4. What Update does today, part by part

Local evidence for this section is `SKILL.md` **Update**, `catalogue.load/adopt/_adopt_models/_adopt_plans/_model_fault/_card_fault`, `setup_apply.apply`, `launch.definitions/sync_definitions`, `profiles.load`, and `evidence.UNKNOWN_CAPABILITY`, read at `1895c21`.

| Part | Current behavior | Unattended disposition |
|---|---|---|
| Source reading | Opens every known model/plan `source_url`, plus provider pricing pages where needed; agent writes scratch JSON | Yes, headless reader can do it. Add authoritative model-index/release discovery so new models have an entry point. A blocked/partial page is a failed refresh, not absence. |
| New model records | Field merge; new IDs with provider/family and attribution are admitted | Yes. Keep exact canonical identity and separate channel launch ID. Existing profile leaves them disabled. Automatic routing enrollment needs an explicit policy change, below. |
| Model removal | **Not implemented.** `load` unions seed and refreshed by ID; `adopt` only adds/replaces. Omitting an ID never removes it | Add durable retirement/access state that masks active entries, including seed entries. Deleting a refreshed row would resurrect its seed. |
| Prices | Reads USD/MTok base and long-context cards, threshold and reasoning billing; writes source/retrieval metadata | Yes with strengthened validation and a visible before/after record. Preserve known facts when source evidence is missing. Include serving tier, cache TTL and context cliff in the evidence. |
| Plans | Replaces the list for each provider represented by valid submitted plans | Yes for public offerings. A partial page must not erase unseen plans. Current representation cannot explicitly replace a provider's list with an empty list; all-rejected plans leave the old list. Actual purchased plan remains a user fact. |
| Deliberation | Adopts supported levels from the fixed low/medium/high/xhigh/max vocabulary | Yes for verified model-and-harness controls. New vocabulary/launch mechanisms need implementation; do not silently map them to a different measured point. |
| Aliases, release date, provider description | Adopts published facts, merging supplied fields | Yes. Do not invent dates or capability numbers from prose; validate aliases before using them to merge identities. |
| Capability seeds | Ignores and reports any offered `capability`; preserves existing seed. A new model has null capability; estimator uses `UNKNOWN_CAPABILITY = 0.5` | No research action needed. Preserve this behavior. Automatic benchmark ingestion is neither today's Update nor necessary for lifecycle maintenance. Local exploration can accumulate evidence without ageing old rows. |
| Profile, payment channels, custom gateway rates | Update does not change them | Preserve user choices. Public discovery cannot infer a purchased plan, a negotiated rate, or willingness to pay a new provider. A fresh provider price does not override a user rate. |
| Generated agents | Runs `setup_apply.py` without a profile operand, which syncs definitions without writing the profile | Yes through the trusted controller. Sync after successful state adoption; retry/report partial sync failures. |

Important details that the short Update prose hides:

1. **The validator checks shape, not truth.** `source_url`/`retrieved` must be nonempty, but neither source authorship nor date freshness is proved. Currency/unit and ladder membership are checked; a plausible wrong USD number passes. `_card_fault` does not validate every price member as a finite, nonnegative number. Whole-field merging also means a newly supplied partial `price` object can lose omitted categories. Stronger validation is a prerequisite to unattended price changes.
2. **The current report is too weak to be the permanent audit trail.** Model reports name changed fields, not old/new values. Plan reports compare names, so a plan whose price changed under the same name can be reported `unchanged`. The report is rendered to the interactive user, not saved as a durable lifecycle change journal.
3. **New-model discovery is not automatic enrollment.** The current Status instruction explicitly says adoption of a newly discovered model into the profile is the user's act. To fulfill “new ones must come in” as active routing candidates, choose and document a one-time automatic-enrollment policy: recommended scope is newly verified models on already approved provider/payment channels, within explicitly approved families/task capabilities, preserving individual exclusions. New providers, subscriptions and changed payment arrangements still need setup. Store policy separately from facts and compute effective eligibility; do not silently rewrite the user's old seven-ID allowlist. Successful minimal channel validation can precede enrollment; #304's measured-point preference and exploration then govern how a new model earns work.
4. **Gateway rates on this machine are a user override.** The saved Grok card is input/cache read/cache write 0.9915 and output 6.174 USD/MTok; today's gateway metadata says base input 2/output 6/cache read 0.5, with no cache-write figure. This is a reportable disagreement, not authorization to overwrite the profile. If future automatic gateway rates are desired, distinguish fetched per-model/channel cards from deliberate user overrides. `docs/research/model-and-price-facts-2026-09.md` already documents why gateway and direct-provider prices cannot be interchanged.
5. **Agent filenames are by family and deliberation, not immutable model ID.** `definitions` selects the newest enabled model in a family (release date, then ID), so two releases compete for the same `kntnt-<family>-<level>.md`. There are 15 requested files on this profile, five each for Fable, Opus and Sonnet. Removal means deleting a now-unwanted file or rewriting it to the remaining eligible release in that family. `sync_definitions` only removes `kntnt-*.md`; preserve unrelated files. Existing sessions may already have loaded an old definition; regeneration cannot revoke that in-memory state or cancel work already running.

**Uncertain:** complete source coverage for subscription plans, credentials held on other machines, and the intended scope of automatic enrollment. The findings propose a bounded scope; implementing the new behavior must make it explicit. None requires keeping manual price-refresh labor as the normal path.

## 5. When is a model gone, and what remains?

**Proposal: three consecutive qualifying daily observations, on separate passes spanning at least 48 hours, for the same exact model and namespace/access path.** A pass qualifies only after successful retrieval/validation of authoritative absence evidence; a missing ID in a picker, a filtered user list, a failed HTTP fetch, or an ambiguous generation error does not qualify. The count is debounce against publication/routing mistakes, not a statistical proof. A clear first-party effective retirement notice supplies the meaning of absence; preserve its effective date and scope.

Use two distinct conclusions:

- **Unavailable on an approved channel:** the account cannot currently launch it there. Record the concrete account/channel reason and suppress that route when sufficiently established. A model available through another approved channel remains usable. Auth/quota/outage is channel health, not a model retirement record.
- **Retired in the relevant model namespace:** authoritative evidence establishes that exact version/ID no longer exists there. A gateway's retirement does not assert the original provider retired it. Only an original-provider retirement notice/appropriate authoritative provider evidence can support that broader statement.

A successful availability result resets the sequence and can restore a route. An outage, auth/quota failure or ambiguous pass **breaks the consecutive sequence** without retiring anything; retain the diagnostic history. Thus “not found, outage, not found” is not three strikes. Never use the grader's `MAX_ATTEMPTS = 3` as this policy: it counts different failures for a different purpose. Three repetitions of the locally observed Claude 404 or Codex 400 remain ambiguous forever.

After confirmed retirement:

1. Exclude the entry from **active selection and alias resolution**, including masks over both the shipped seed and refreshed catalogue. Retain an archived record/tombstone with the version ID, sources, dates, namespace, last-known facts and the three observations. A later refresh or collection upgrade cannot resurrect it simply by omitting the tombstone. A confirmed reintroduction is a new audited lifecycle transition.
2. **Keep all measurement rows unchanged.** No deletion, decay, repricing of historical dollars, grade changes, or copying rows to a successor. They remain queryable history; reactivation of the same release can reuse them. Probe and lifecycle failures never enter this store as task grades.
3. Preserve the user's selection/exclusion intent, but report enabled IDs that are now unavailable. Do not rewrite a paid channel because a model disappeared. Make effective eligibility intersect intent with lifecycle availability.
4. Regenerate owned Claude definitions against effective active eligibility. Remove now-unused `kntnt-*` files, or rewrite a family filename to the remaining eligible release; leave all unrelated definitions intact. Check locks and explicit names against active availability. A caller that must honor a user lock still detects an unhonored lock locally; the selector's inherited-seat fallback must keep answering.

**Evidence:** additive `catalogue.load/adopt` and prefixed `launch.sync_definitions` show why a tombstone/eligibility layer is needed. The local bogus calls and first-party error meanings in §2 show why a generic exit status or 404 cannot decide this transition. The immutable-behavior premise is supplied by the maintainer, not inferred from ageing tests.

**Uncertain:** there may be channels where no authoritative absence source is accessible. On those channels the honest outcome is persistent unavailable/unknown with visible evidence, not fabricated certainty. This does not stop new-model discovery or fact maintenance elsewhere.

## 6. ADR-0185 and making changes visible

**Yes: implementing this design supersedes ADR-0185's restriction to person-invoked fetching and its conclusion that nothing reaches the network unattended.** Its valuable split survives: an agent interprets the world; deterministic code decides what enters the store. A headless agent has the missing interpreter, so the finding that the old fetch-only script learned nothing does not imply automation is impossible.

The replacement must change the last paragraph of `docs/rules/routing.md`, the affected Skill/help/status/setup wording, and owned-integration descriptions together. Write the decision under **the next free ADR number at implementation time**, naming the old premise, the new evidence and the accepted residual risk. Leave ADR-0185's historical body unchanged under `docs/rules/docs.md`. This research changes neither rule nor ADR.

**Proposal for application and visibility:**

- The reader emits a staged bundle: candidate field values, exact first-party source URL, retrieval time, source digest and the relevant table/row context. Keep rate basis explicitly identified: direct or gateway, Standard/Batch/Flex/fast, cache TTL, USD/unit, threshold and whether the higher tier reprices the entire request. Do not turn a blocked page into a new retrieval date for facts not actually read.
- A deterministic check compares complete old/new values. Reject invalid/nonfinite/negative rates, unsupported controls, incomplete price cards, contradictory tiers and fabricated attribution. Missing data preserves last-good values or stays explicitly unknown for a new entry. A large change is not necessarily wrong; use it to require corroboration, not to silently clamp the price.
- Corroborate ranking-affecting price changes with a second first-party representation, or a second separately fetched reading when only one page exists. A repeated reading can repeat a misinterpretation, so this reduces risk without proving truth. Unresolved discrepancies stay **unapplied**, named with sources; they do not block unrelated valid entries or routine selection.
- Persist a durable revision journal **before the new facts become active**: revision ID, old/new values, reasons, sources/digests, discovery/access transitions, validation/discarded entries, budget and outcome. Use a recoverable commit marker and a shared writer lock; the current single-file atomic rename does not make catalogue, journal and generated agents one transaction. A failure to make the change auditable must prevent its activation.
- `/model-selector status` shows last attempt, last successful refresh, oldest/newest verified source dates, next due time, unavailable/unknown/retired models, newly enrolled or disabled models, deferred work and failures, and **every unacknowledged applied revision** with old/new values and sources. “No changes” must be distinguishable from “could not check.” Report definition-sync failure explicitly.
- Put the active fact revision in selection answers and a short note when an unacknowledged ranking-affecting change exists; callers must surface that note in their ordinary human-facing report. Showing Status can mark a revision seen through an explicit presentation/acknowledgment mechanism; an unattended metadata read must not consume the notice. Keep rollback to the last good revision available. No approval queue or prompt is inserted into delegated work.

Illustrative Status content, **not an actual applied change**:

```text
Daily lifecycle: last attempt 11 Sep 03:00; complete; next due 12 Sep 03:00.
Facts revision 24, not yet acknowledged:
  model X input USD/MTok: 4 -> 2; output: 20 -> 10.
  Source and rate basis: <first-party URL>, Standard, retrieved 11 Sep.
  model Y: retired on channel Z after 3 qualifying daily observations.
  Measurements retained; 5 owned definitions removed; no profile changes.
Deferred: model Q price sources disagree; revision 23's rate remains active.
```

This makes adoption **durably visible**, including to a user who does not routinely run Status. It cannot guarantee that a human reads a notice. If “never silent” instead means “no price change may affect rankings until a person has reviewed it,” require pre-activation acknowledgment for prices; that is a different policy with unavoidable human latency. The recommended policy is automatic corroborated adoption plus persistent notice, with disputed changes held. It removes routine Update work without pretending that a page reader cannot misread a price.

**Uncertain:** first-party sites do not always provide two independent price representations, and unattended interpretation cannot be made infallible. A status/journal feature mitigates the original silent-ranking risk; it does not validate semantic truth by itself.

## Verification and cleanup

Only this findings file is a repository deliverable. No application code, catalogue/profile, measurements, generated definitions, scheduler or GitHub issue was intentionally modified. The full end-to-end maintenance pass remains future work, not a tested implementation.

The four checks in `CONTRIBUTING.md` passed: Ruff lint, Ruff formatting (306 files), mypy (56 source files), and pytest (**1,404 passed**). Test/cache output was redirected to temporary storage. The first pytest run had three teardown failures because the redirected `KNTNT_HOME` directory did not exist; creating that directory and rerunning the full suite resolved them without source changes. Markdown fences, the six question sections, the final ticket-breakdown section and the staged whitespace check were also verified.

One setup mistake was disclosed during the investigation: the cleanup helper initially appended this scratch directory's registration to `~/.kntnt/session-cleanup/sessions/terminal-27444.jsonl`. That single own record was removed (the file was removed if empty); subsequent registrations used a scratch-local `KNTNT_HOME`. This was an exception to the requested no-write boundary, not a Model Selector state mutation. Read-only hashes of all five files under `~/.kntnt/model-selector` matched after the probes. A later check found that another ongoing session had appended its own pending work; those unrelated rows were left intact. Profile and catalogue bytes still matched. Temporary credentials, source notes, CLI state and scratch files were removed; all investigation-owned process groups were stopped.

## Proposed ticket breakdown

These are proposed titles/dependencies/deliverables only; none was filed. Vantage point: `1895c21`. The existing chain #303–#307 is not redefined here. Read those tickets' full threads before implementing work that touches their surfaces. References to source symbols are intentional; line numbers will drift.

| ID | Proposed title | Blocked by | Delivers |
|---|---|---|---|
| L1 | Make Model Selector's process launches match the installed harnesses | None | Correct OpenCode cwd and gateway/model-ID translation in `launch.plan/_opencode`; preserve actual deliberation identity instead of claiming a different executed level. Establish versioned launch/error envelopes and tool-free probe controls with isolated contract tests. Recheck existing launch fixes before doing overlapping work. |
| L2 | Discover models and classify channel availability without inference by default | L1 | Claude SDK/control and Codex `model/list` adapters; OpenCode catalogue plus OpenRouter user/public metadata adapters; pagination, freshness and exact-ID mapping. A normalized distinction between model absence, access/config failure, quota, outage and timeout. One bounded optional probe per model/pass; ambiguous evidence never means retired. |
| L3 | Record lifecycle transitions while preserving all measurements | L2; #307 to integrate after the existing selection changes | Three-day qualifying-absence state machine, namespace/channel distinction, seed-safe tombstones, active eligibility/alias filtering and reactivation. Explicit automatic-enrollment scope and preserved exclusions/payment choices. Sync only owned definitions to effective eligibility; retain all measurements and inherited-seat fallback. |
| L4 | Stage and validate headless world-fact readings with a durable change journal | L1 | Restricted researcher adapters for all three harnesses; field-level source evidence, complete rate/tier validation, explicit empty-plan replacement, before/after reports, corroboration and last-good retention. Recoverable journal/adoption/sync protocol; user rate overrides and capability seeds preserved. Offline fixtures test semantic misreads and interrupted application. No automatic network trigger yet. |
| L5 | Surface lifecycle health and every unacknowledged fact change | L3, L4; #305 and #307 for their Status/answer changes | Status dates/outcomes/errors, old/new values and sources, unacknowledged revisions, definition-sync health, revision-bearing selection answers and required caller notice. Recovery/rollback path. No hidden “healthy but learned nothing” state. |
| L6 | Run one bounded daily lifecycle pass and retire manual Update maintenance | L2, L3, L4, L5 | Owned daily scheduling on the current Mac, portable harness dispatch, idle/wake behavior, one lock/attempt per day, strict wall deadline, spend reservation/reporting and paid-channel budget enforcement. Prevent recursive hooks; disable/uninstall stops owned scheduling. Supersede ADR-0185 under the next free number and sweep routing/Skill/help/setup/update documentation. Retire `update` as the required maintenance verb; optionally retain a compatibility rerun entry point to the same controller. Test headless staging/adoption/sync against disposable data/agent directories on each harness before release. |

L4 can proceed beside L2/L3 after L1. L6 is the first ticket that enables unattended network activity, and is blocked until visibility and recovery exist. Each eventual implementation ticket must carry the four checks in `CONTRIBUTING.md` as acceptance criteria, cite the commit it was written against, and re-read current rules/state rather than assuming this snapshot survived unchanged.
