# Model Selector: what a cross-family run cost, and why it was chosen

Researched on **2026-09-20**, against `main` at `65834c32`, on the maintainer's Mac, for issue #368. This is a findings document, not a change to the current rules. The seven decisions at the end were taken by the maintainer in the triage session of the same day; each is carried out by an ordinary ticket, and until that ticket lands `docs/rules/routing.md` says what holds.

Everything marked **measured** was read from the machine's own store (`~/.kntnt/model-selector/`, 698 rows), from Codex's session logs under `~/.codex/sessions/`, or reproduced by importing `evidence`, `catalogue`, `profiles` and `selection` from `skills/models/model-selector/scripts/` and ranking the real data. Nothing under `~/.kntnt/`, `~/.codex/` or `~/.claude/` was written.

## Verdict

**Delegating across the family boundary is not dearer per token in any way the rate card misses. It looked cheaper than it was, was chosen on an estimate nobody had tested, and the comparison it won was not like for like.** Four things produced the 2026-09-19 outcome, in order of weight:

1. **An untested estimate beat the best-measured point on this machine.** `gpt-6-astra@high` won `implement` with no rows of its own, at 16.74 USD per finished job, over `claude-opus-5@high` at 7.01 USD with 142 rows, because the first cleared the floor of 0.8 on a formula and the second missed it on measurements.
2. **The two prices compared were prices of different things.** The Opus forecast is 96 % the main session's own short spans; the Astra rows are whole ticket builds. A routed Claude build carries no token counts at all.
3. **List-price dollars are not quota.** The ranking orders on one USD figure, and what ran out was a weekly subscription window whose size in those dollars nobody had recorded.
4. **Once nothing clears the floor, price stops mattering.** The ranking falls back to the likeliest point whatever it costs.

## What happened

An Orchestrate run on 2026-09-19 asked Model Selector 22 times from a `claude-opus-5@high` Claude Code seat, ranked on cost. The first builds went to `gpt-6-astra` through the Codex Bridge. The six Codex attempts, **measured**:

| attempt | list price | seconds | grade | weekly window | Δ points |
|---|---|---|---|---|---|
| build, `high` | 12.47 | 2949 | 1.0 | 0 → 1 % | +1 |
| amend, `medium` | 6.49 | 1349 | 0.6 | 3 → 4 % | +1 |
| build, `high` | 19.21 | 1900 | 0.0 | 4 → 6 % | +2 |
| build, `xhigh` | 36.15 | 2779 | 1.0 | 7 → 9 % | +2 |
| build, `xhigh` | 20.93 | 2189 | 1.0 | 9 → 11 % | +2 |
| build, `xhigh` | 34.96 | 2959 | 0.0 | 11 → 13 % | +2 |
| **total** | **130.21** | | mean 0.6 | **0 → 13 %** | **+10** |

The ChatGPT Pro 20x window went from 0 % at 08:52 UTC to 95 % at 23:51 UTC the same day; the maintainer was using Astra in his own work alongside the run, so the run's share is the 10–13 points above. That puts the weekly window at roughly **10–13 list-price USD per percentage point, or 1 000–1 300 USD a week**, on six samples quantised to whole points. Astra's token forecast was about right (13.92–26.38 forecast against 12.47–36.15 measured): the selector knew Astra was two to four times dearer and chose it anyway.

## Finding 1 — the floor, and what clears it

`_ranked` in `selection.py` splits the pool at `FLOOR = 0.8` on the posterior mean before price is read. Points that clear it are ordered on price per finished job; the rest follow ordered on chance alone. `_vouched` puts a point measured for the kind first only where that point itself clears the floor (issue #304).

Replayed as the store stood before the run (597 rows), `implement`, scope `callable`, objective cost, ceiling `xhigh`:

| # | point | basis | mean | low | n | USD/job |
|---|---|---|---|---|---|---|
| 1 | gpt-6-astra@high | prior | 0.832 | 0.629 | 0 | 16.74 |
| 2 | claude-fable-5-1@xhigh | pooled | 0.810 | 0.612 | 1 | 17.30 |
| 3 | gpt-6-astra@xhigh | prior | 0.858 | 0.669 | 0 | 20.45 |
| 5 | claude-fable-5-1@high | measured | 0.763 | 0.631 | 12 | 14.24 |
| 6 | claude-opus-5@high | measured | 0.749 | 0.702 | 142 | 7.01 |

Only three points cleared the floor and none was measured, so the measured-first guard never engaged. Astra's 0.832 is arithmetic, not evidence: `sigmoid(SHARPNESS × (capability + bonus − difficulty))` = `sigmoid(8 × (0.90 + 0.05 − 0.75))`. To clear 0.8 on the prior alone at `high`, a model's seeded capability must be at least 0.873; `claude-opus-5` is seeded at 0.87. **Three thousandths of a seeded figure decided the run.**

Replayed now (698 rows), nothing clears the floor. The whole list is ordered on chance, and `gpt-6-astra@xhigh` at 38.99 USD per job sits second, ahead of `claude-opus-5@high` at 8.21.

Alternative rules, replayed against both snapshots:

| rule | before | now |
|---|---|---|
| current | astra@high, prior, 16.74 | opus@xhigh, 9.99 |
| an unmeasured point must clear the floor on its lower bound | astra@xhigh — still wins, through the fallback | opus@xhigh, 9.99 |
| measured only, cheapest per finished job outright | gpt-5.6-luna@low, mean 0.18, 1.16 | the same |
| floor lowered to 0.7 | opus@high, 7.01 | opus@high, 8.21 |
| **measured only; cheapest per finished job among the points whose mean is at least the best measured point's lower bound** | **opus@high, 7.01** | **opus@high, 8.21** |

The third row is why dividing by the chance is not protection enough on its own: the cheapest junk in the pool wins. The last row is the rule adopted. It uses the uncertainty the estimator already computes and adds no constant.

## Finding 2 — the comparison was not like for like

**Measured**, whole store:

| routed | family | tokens present | rows |
|---|---|---|---|
| yes | Claude | no | 145 |
| yes | Claude | yes | 10 |
| yes | GPT | no | 34 |
| yes | GPT | yes | 6 |
| no | Claude | yes | 501 |

Orchestrate's `observed_measurement` files a routed row with whatever `--metrics` gave it. A Codex builder run with `--json` exposes its usage; a Claude subagent does not, so the row arrives with `"tokens": {}` and `record.py` declines to price it. The path meant to repair this exists — `capture.py` reads the builder's own transcript, and a brief opening with `attempt_id: <id>` is meant to fold that Unit into the row Orchestrate filed (issues #291, #303) — and is inert on this machine: none of the 145 rows has an `attempt_id` matching a captured Unit, and every pending Unit carries a `unit-<hash>` identity. The cause, **measured**: the match is made on the first line of the subagent's first user message, and the dispatching session hands a builder a pointer to a brief file rather than the brief — 222 subagent records on the machine open *"Your whole brief is the file …"*, and the five that open with the `attempt_id:` line are the five routed Claude rows that merged. Separately, `grade.py` files every row it writes as `routed: false`.

So for `claude-opus-5` × `implement`, 213 rows: 75 routed rows contribute a grade and no price; 132 non-routed session spans, median 608 seconds and 7.01 USD, supply the price. The chance of success and the price rest on largely disjoint rows, and the price is that of one span inside a session, not of one build. An Astra row is one whole build of 25–50 minutes. One Opus build that produced four captured spans is four cheap rows; one Codex build is one dear row.

Two smaller distortions, **measured**:

- Codex reports `cache_write: 0` on every row. `Estimator._normalised` skips values that are not positive, so the forecast falls back to the kind's shipped prior and prices about 239 000 cache-write tokens Codex never bills: roughly 3 USD per attempt at `high`, 3.64 at `xhigh`. A measured nought is a measurement.
- Delegated Units are exempt from `OWN_UNIT_SECONDS`, and the store holds `implement` rows of 274–424 seconds from 2026-09-19, each a cheap row.

## Finding 3 — exploration only goes downhill

`_below` admits an exploration candidate only where it is cheaper than the plain answer, so **no route exists by which a dearer untested model is tried once any measured point clears the floor.** For a cheaper one, a plain call explores with probability 0.1, the coin gives the model dimension half of those, and the draw is shared among every cheaper rival. Simulated over 200 000 calls against the live pool, a never-measured model in the middle of the cheaper pack (`gpt-5.6-terra@xhigh`) receives 0.40 % of calls: about **750 build calls for the three rows** that make a point measured (`ENOUGH = 3`), and fewer still in practice, a first failure collapsing its posterior. Orchestrate passes no `--seed`, so the draw is per call.

Exploration does its other job well: about 5 % of calls try the answer's own model at a lower level.

## Finding 4 — quota can be read

- **Codex, per turn, on disk.** Every `token_count` event in `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` carries `rate_limits.primary` with `used_percent` (whole points), `window_minutes` (10080, the week) and `resets_at` (Unix seconds), plus `plan_type`. Concurrent sessions each hold their own last-fetched value, so the machine-wide figure is the latest across files.
- **Claude Code, as a snapshot.** The status line's standard input carries `rate_limits.five_hour` and `rate_limits.seven_day`, each with `used_percentage` and `resets_at`. This was read off the maintainer's own status-line script and must be checked against Claude Code's documentation before anything is built on it. The per-model weekly windows are not in that payload. No per-turn history exists: transcripts carry no rate-limit fields, so Claude's consumption on 2026-09-19 cannot be reconstructed.

## Decisions

Taken by the maintainer on 2026-09-20. Each changes what Model Selector promises a caller, so each is recorded in a decision record by the ticket that carries it out.

1. **A point measured for the kind comes before one that is not, in every plain answer** — not only where the measured point clears the floor. An untested estimate never again beats what the machine has seen.
2. **Where no measured point clears the floor, the answer is the cheapest per finished job among the measured points the evidence cannot tell from the best** — those whose mean is at least the best measured point's lower bound. The floor of 0.8 stays as the first step where a measured point does clear it.
3. **A model with no measurements of its own for a kind gets a trial: three reversible jobs of that kind, whatever it costs, at the level nearest the answer's.** After that it is judged on its own rows. Only a model that could plausibly win is owed one: its estimate is at least the best measured point's lower bound for the kind, the band of decision 2. Replayed against the store on 2026-09-20, the unfiltered rule owed `implement` fifteen consecutive Trial builds on five models the prior put at 17–46 %; with the band it owes none, and would have owed `gpt-6-astra` one on 2026-09-19. One model at a time per kind; no price cap; the deliberation ceiling and the quota guard still apply. The one-in-ten downhill exploration stays as it is.
4. **Quota is a guard, not a currency.** Ranking stays on list price. A subscription channel is taken out of a machine-chosen answer while its weekly window is more than ten points ahead of the share of the week elapsed, or at 90 % used whatever the pace. The guard never empties the pool — where every channel is held back they are ranked as usual — never stops a model the user locked, and a held-back channel gets no trial jobs. Ranking on quota consumed was considered and set aside: whole-point resolution, concurrent sessions and the maintainer's own use make a per-attempt figure mostly noise, and the harm to prevent is the window running out.
5. **Claude's figure comes from a documented file the user's status line writes**, in Model Selector's data directory, in a shape `docs/rules/routing.md` states; `setup` shows the line and offers to add it. No network call, no credential read, and the same for every user of the collection. No file, or a stale one, is no guard for that channel, said nowhere and refused never. Codex's figure is read from its session logs directly.
6. **Two defects are fixed as defects**: routed Claude work gets its token counts, and a measured nought in a token category is a measurement.

7. **Where a newer release of the same model family exists, no older release is chosen** — Grok 4.3 and 4.5 are not candidates while Grok 4.6 is offered. A family is what the catalogue states, a lock on an exact id is still honoured, and nothing stored is removed.

The tickets: #370 and #371 (decision 6), #372 (decisions 1–2), #374 (decision 3), #373 (decisions 4–5), #375 (decision 7).

Decisions 1–2 and 3 ship together: the first closes the door on untested models and the third opens the one they come in by.
