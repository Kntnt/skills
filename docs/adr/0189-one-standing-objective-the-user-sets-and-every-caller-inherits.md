# One standing objective the user sets, and every caller inherits

This record amends the rule in [`docs/rules/routing.md`](../rules/routing.md)'s paragraph on what finishing is counted in: *What finishing is counted in is the caller's to choose, and money is the default*. That rule began alongside [ADR-0182](0182-how-a-model-is-chosen-and-how-the-choice-is-measured.md), which does not itself argue the objective. The rule was that a caller may pass `--objective=time`, and that an answer asked for with none ranks on cost. It now reads: the caller's `--objective`, else the user's standing choice, else cost. What the rule now is is stated in the rules module and in the Skill's own shipped files. This record argues the case.

## What the old rule missed

**Which objective is right is a fact about the user, not about the caller.** It turns on how much of their subscription quota is left this week. With room to spare they want results as fast as possible. When the quota runs short they want the cheapest way to finish. No calling Skill knows which week it is.

**One flag per caller is one flag per caller for one fact.** Under the old rule, only Orchestrate's `--fast` ever asked for time. Giving /delegation a flag of its own, and every later caller one after it, would ask the user to say the same thing in as many places as there are callers, and to say it again every time the week turns.

## The rule

**Model Selector keeps one standing objective.** `/model-selector objective time` and `/model-selector objective cost` set it. Bare, the verb says which is in force and whether it is the standing choice or the default. The words are the existing `--objective` vocabulary and no new one.

**The order is the caller's, else the standing choice, else cost.** An explicit `--objective` wins in both directions, so `/orchestrate --fast` still orders its run on time. With nothing set the default stays cost. Running out of quota mid-week stops everything, while a slower job is only slower. After [ADR-0188](0188-the-price-of-a-finished-job-orders-what-clears-the-floor.md), cost means the cost of getting the job done, not the cheapest attempt.

**The answer says what it ranked on.** Every answer, an inheriting one included, carries `objective` (`time` or `cost`) and `objective_source` (`caller`, `standing` or `default`). Two callers asking the same question with no `--objective` are answered on whatever the user last set, and a reader has to be able to see which.

**It is kept on its own, and read fail-open.** The choice lives in `objective.json` in the data directory and not in `profile.json`. Writing the profile replaces it whole on every `setup`, which would drop the choice, and a profile holding only an objective is not a profile that loads. `setup_apply.py` writes the file through its own option; `selection.py` only reads it, being the machines' interface. A file that cannot be read, or names a word other than `time` or `cost`, is treated as absent: the answer uses the default and its note names the file. The call is never refused. `reset` removes the file, the choice being an answer the user gave.

**What nobody waits on is pinned to cost.** The judge that grades a finished unit is asked for with `--objective=cost` by name. The standing choice is about work somebody is waiting on, and nobody waits on a grade.

**A run holds the objective it began with.** Orchestrate promises that the objective is held for the whole run. It records the `objective` its first routing call was answered with and passes it as an explicit `--objective` on every later request of that run — amend, repair and rebuild included, and on resume. A standing choice flipped mid-run reaches the next run. An answer that names no objective, from an older Model Selector, records nothing, and nothing is passed.

## The alternatives

**A flag on every calling Skill.** Rejected. It is one flag per caller for one fact about the user, and the user would have to keep them all in step.

**Keep the choice in `profile.json`.** Rejected. The profile is replaced whole by `setup`, so the choice would not survive the interview, and a profile holding nothing but the choice fails to load.

**Make time the default.** Rejected. Running out of quota stops all work until the week turns, while ordering on cost only makes a job slower. The costlier failure is the one the default has to avoid.

**Let Orchestrate read the standing choice afresh on every call.** Rejected. A run ordered on time for its first wave and on cost for its last is not one run, and Orchestrate already promises that the objective is held for the whole of it.
