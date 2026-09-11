# A model its maker stops listing is removed, with its measurement

This record extends [ADR-0191](0191-a-script-keeps-the-catalogue-current-from-three-structured-sources.md), whose pass reads every chosen maker's list, and it ends the rule that measurement rows are kept until somebody discards them by hand. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What was wrong

**A model that no longer existed was never removed.** `catalogue.load` merged the shipped seed and the refreshed catalogue by id, and `adopt` only added or replaced entries (`docs/research/model-lifecycle-2026-09.md`, section 4). Deleting a refreshed entry by hand only brought the seed's copy back. So a retired model went on being a candidate, and its agent definitions went on being generated, for as long as the Skill was installed.

## The rule

**A model is gone when its maker's complete list lacks it on three consecutive UTC days.** A day is absent where at least one complete read that day lacked the model and none showed it. A day on which any complete read showed it resets the run, and a day with no complete read breaks it. The first complete read on the third consecutive absent day removes the model. Three days is a debounce against a vendor's list being wrong for a day, not a proof.

**Presence is judged on the version identifier each list names, and never on an alias.** A family alias such as `opus` moves to each new release, so matching on it would keep a replaced release present for ever. A Claude entry is its `resolvedModel` without the bracketed serving selector, so `claude-opus-5[1m]` is `claude-opus-5`. A Codex entry is its `model`. An OpenRouter entry is its full id, compared with the model's id and with its OpenRouter slug, which the same pass writes back before presence is judged. A literal comparison of ids with no such rule would have deleted the most-measured model on the machine after three days. An entry the Codex list returns marked hidden counts as present, since deletion cannot be undone and the list still returns it.

**When a model is gone, it goes everywhere at once.** Its catalogue entry is removed. A record in `lifecycle.json` in the data directory masks the seed's copy, so no later load or release of the seed brings it back. Every measurement row and pending Unit with its exact id is deleted. The generated agent definitions are resynced, so a family's definition either moves to the release that remains or is removed. The removal is journalled with its three dates and two counts, the rows deleted and the Units dropped, and `/model-selector status` shows every removal for as long as `lifecycle.json` records it.

**The lifecycle state lives apart from both the catalogue and the evidence.** `catalogue.json` is rewritten whole by `adopt`, so a mask kept there would be lost. The measurement store is what `reset --evidence` discards, and a removal is a fact about the catalogue rather than about this machine's measurement. So `lifecycle.json` is its own file, and `reset --evidence` leaves it alone.

**A removed model that comes back is an ordinary model.** The mask covers only the seed's copy. When the id reappears in `catalogue.json`, through the pass or through `adopt`, its mask, its removal record and its absence history are all deleted in the same operation. From then on no pass deletes anything for it. Nothing deleted in between is restored.

**The deletion runs under the grading lock, and is repeated.** `grade.py`'s lock moved into `evidence.py`, the module that owns the measurement ledger, so there is one lock for both. Where another pass holds it, the entry is still removed at once and the rows wait for the next pass that gets the lock. Capture appends without any lock, so rows for a removed model can arrive after the removal, and every later pass therefore deletes rows and Units for each id in its removal record, a pass choosing no maker included.

## Why failing to run is never the signal

**A quota would otherwise read as a mass extinction.** A weekly subscription quota running out stops every GPT model for days. Counted as evidence, it would remove all of them after three days, together with every row that says how good they are. Quota, outage, authentication and access failures are the channel's health, and they say nothing about whether the model exists.

**The harnesses cannot tell "no such model" from "no access".** Sections 2 and 5 of the findings recorded Claude Code's 404 and Codex's 400 for a model id that does not exist, and the same shapes for a model the account may not use. Three repetitions of an ambiguous answer are still ambiguous.

**So only a list that was read successfully and completely counts.** A source that failed, or that looked truncated, is no observation, and it breaks the run of three rather than extending it. A pending Unit that failed to reach a judge three times is left to the grader's own rules and removes nothing.

## Why the rows are deleted

**The maintainer decided on 2026-09-11 to delete them, over the findings' advice to keep them.** The findings proposed keeping every row as history that a reactivated release could reuse. The maintainer's premise is that a model which has left its maker's list does not come back. Its rows are then worth nothing to a selection that can no longer choose it. Kept, they would go on shaping the pooled estimates of the kinds they measured, on behalf of a model nobody can launch. The same goes for its Units waiting to be graded, whose judgement would be bought for nothing.

## The alternatives

**Keep the rows, and archive a tombstone with the last-known facts.** Rejected by the maintainer, as above. A tombstone is also left out: the journal and `lifecycle.json` already say when and why a model went, and nothing reads the facts it would keep.

**An "unavailable on a channel" state that suppresses the route.** Left out. It answers a different question, which channel can reach a model today, and any evidence it could rest on is exactly the failure-to-run signal rejected above.

**Count the harness's "no such model" errors.** Rejected, because those errors cannot be told from "no access".

**Treat a model the list returns hidden as absent.** Rejected. Deletion cannot be undone, and a vendor hiding an entry has not stopped returning it. The pass still adds no hidden entry, which is a different question.
