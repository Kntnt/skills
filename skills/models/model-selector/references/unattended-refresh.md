# Unattended source refresh

Use this reference for `## Status`, and read it beside `run-capture.md` when the question is what a session's end does.

Discovery is `update`'s work and always was: it revalidates provider indexes on a cadence, fetches detail pages for newly discovered version keys, and reports what it finds. Every turn of that loop used to be a thing the user had to remember, so the machine could sit weeks past every cadence answering from a model list nobody had revisited — silently, because no verb reports an empty answer, it reports an answer computed over a stale list.

The unattended pass is that turn, made automatic and made small. It rides the session-end invocation this Skill's lifecycle integration already installs, and it does exactly one thing: validator-conditional retrieval — ETag or Last-Modified, falling back to a content hash — of the non-commercial sources that are due. It is `$HERE/scripts/refresh.py`, dispatched from inside `$HERE/scripts/capture.py`'s existing session-end handling rather than as a second registered hook entry, and it is a sibling of capture on that one seam rather than a part of capture's measurement path.

## What it establishes, and what it never does

**It interprets nothing.** No page is parsed for meaning, no model is started, and no evidence beyond the source's own state is written. The unattended pass establishes *that* something moved; a person's next `update` establishes *what*. A changed source is therefore recorded as changed and never as a discovery, and the `finding` prose and `parser_version` a typed `update` wrote are left exactly as that pass wrote them, this one having made nothing of the source to record.

Of the five `status` values a source state may carry it writes three: `not_due` for a source whose cadence has not elapsed, and `unchanged` or `changed` for one it retrieved. `unreachable` and `invalid` stay the typed `update`'s to write, because both are readings of a source rather than facts about reaching one, and a pass that reads nothing establishes neither. It does not clear one either: where a row already carries an unresolved diagnostic, a look and a retrieval that finds the same bytes both leave that status standing and move only the timestamps, so what the user still has to fix stays in front of them. Only content that actually moved supersedes such a row, the diagnostic then being about content that no longer exists.

It writes `SourceState` rows and nothing else. No capability fact, no benchmark fact, no evidence record and no derived frontier is created, changed or rebuilt by it, and no discovered model is ever adopted — adoption stays the user's act through `config add` or `config edit`, exactly as `update` already decided.

## The commercial split, applied by `kind`

An unattended fetch that mis-parsed a commercial page would write a wrong fact that silently reshapes which model wins, and the user holds knowledge those pages do not state — what a plan actually costs and how a quota actually behaves. So the split is by `kind`, and it is the whole design.

| Retrieved unattended | Never retrieved unattended |
| --- | --- |
| `model_release_index` | `commercial_terms` |
| `model_detail`, though never in practice — see the cadence rule below | `gateway_rate_card` |
| `capability_source` | every other value, including one absent or unreadable |
| `benchmark_release_index` | |

**An unattended pass may change what a model is judged capable of, never what it is judged to cost.** The right-hand column is fail-closed, which is what makes a `kind` added later safe on the day it appears and before anybody has taught this pass about it: such a source is not retrieved, its row is not written at all, and it is reported as due until the user runs `update`. A row whose `uri` is missing, or whose scheme is anything but `https` or `http`, is left the same way — the store is a file a user may hand-edit, and a local path in it must never become a local read.

## Dueness, and the defect this must not reinstall

Cadence is measured from `last_retrieved_at` and from nothing else. A source whose `last_retrieved_at` is absent or null has never been retrieved and is due; that is the state every row written before this pass existed is in, and no migration fills it and no `finding` prose is parsed for it. `last_checked_at` records only that a pass considered the source — a source found not due and a source nothing could reach are both recorded there — and it moves no due date, because measuring cadence from the look would push every source's next due date forward at every session end and nothing would ever become due again.

The cadences are shipped data rather than sentences: `$HERE/data/refresh-cadences.json` holds one per `kind`, and the configuration does not override them. A `kind` with no cadence there is an immutable model detail page, which is never refetched and therefore never due.

## What it costs a session

One connection at a time, no retries, and a total budget of two seconds across the whole pass, enforced in-process rather than by a thread or a timer. The pass runs once per session end and never more. Exceeding the budget, failing, or finding no network surfaces nothing, writes no change to what the store knows about a source, and leaves every unfinished source due for the next attempt. Every failure is swallowed where capture's own are: a refresh that delays a session teardown is worse than a source nobody refreshed.

## What `status` reports

`status` is the one surface this pass is reported on. `route` and its response schema are unchanged and no routed run's account carries any of it, because a measurement reminder placed where the model reads it would change the configuration being measured.

Run `uv run "$HERE/scripts/refresh.py" status --data=<directory>` and render what it returns. It retrieves nothing and writes nothing. Per source it gives the URI, provider and `kind`, whether the pass may retrieve it at all and why not where it may not, the cadence, the last retrieval, the next due date and whether it is due now. Report every due source the pass may never retrieve — commercial terms, rate cards, and any kind or URI it does not recognise — and name `/model-selector update` as what resolves each.

Where `established` is false the store holds no source state at all, which is a machine that has run `setup` and never `update`. Say that unattended refresh has nothing to check and that a typed `update` establishes the sources: the pass itself correctly writes nothing and surfaces nothing there, and a permanently empty pass must not be indistinguishable from a working one.
