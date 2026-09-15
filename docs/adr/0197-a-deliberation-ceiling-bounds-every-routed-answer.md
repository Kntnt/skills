# A deliberation ceiling bounds every routed answer

This record decides how high Model Selector may climb on the deliberation ladder without being asked. Every routed answer is held to a deliberation ceiling. The ceiling is `xhigh` unless the caller passes `--max-deliberation`, and a `--deliberation` lock above it raises it to that lock's level. `docs/rules/routing.md` states the rule as it applies now; this record explains why it has this shape (issue #323).

## What reached the top of the ladder

**`max` was being chosen for work nobody had asked it for.** Sessions in delegation mode spawned subagents on Opus at `max` although the user had never named that level. /delegation had not chosen it: it launches exactly what Model Selector returns. The choice came from the two ways Model Selector's rules reach the top of the ladder. When no candidate clears the floor, the pool is ranked on its chances, and on the shipped priors the likeliest point for hard work is the deepest one. A step up after a failure climbs to any point more likely to succeed, and the last point on the ladder is `max`. Neither rule is wrong for the question it answers, but together they made the most expensive level the usual answer for exactly the work that fails most, with no human decision behind it.

## What the ceiling limits

**The ceiling limits the level, not the model.** The alternative considered was to limit the model as well, keeping the strongest models behind the same opt-in. The user chose the level alone: Fable at `xhigh` is an ordinary answer, and only `max` and anything above it need asking for. Every model shares the one ladder, so a single rule covers all of them. A ceiling on models would have to name models, and would have to be revised every time a new release came out.

**The ceiling does not depend on the caller's own seat.** An earlier idea was that a spawn may never be stronger than the session that spawns it. It was dropped: an orchestrating session on a small model doing mechanical work is exactly the caller that should be able to route a hard job to a stronger model. What must not happen unasked is the top of the ladder, whoever asks.

**The ceiling is compared by position on the ladder, not by name.** A level added above `max` later is excluded by the default without anyone listing it. A point with no effort control has no level, so the ceiling does not apply to it.

## Why a flag of its own, and not the lock

**The first draft of the ticket made the existing lock the opt-in, and that was wrong.** `--deliberation=max` pins every answer to `max`. It cannot express *`max` is allowed where the evidence calls for it*, which is what someone lifting a ceiling means. A ceiling narrows the choice and pins nothing, so it is a separate flag, `--max-deliberation`. With that flag the ceiling can also be lowered, which a lock cannot do.

**A lock above the ceiling raises the ceiling to the locked level and no further.** The user named that level, and an explicit choice wins. Raising the ceiling only as far as the lock stops the fallback to a model's nearest supported level from climbing past the level the user named. The answer says when a lock lifted the ceiling, so an answer at `max` always shows who asked for it.

## Where it lives

**The rule belongs to Model Selector, and every caller gets it without having to do anything.** `routing.md` forbids a caller from reproducing selection policy. A ceiling written into /delegation would have left /orchestrate's builders and the grader's judge still reaching `max`. Callers only pass a ceiling the user gave: /delegation adds it to its one routing call, and /orchestrate holds it for the whole run, beside its locks and on the same terms as `--fast`.

**Callers are never refused.** The ceiling runs inside another Skill's turn, like the rest of Model Selector, so it never refuses. Where it empties the pool, the answer is the caller's own seat, with a note naming the ceiling. Where it changes the answer, the note names the point the same call would have chosen without the ceiling and without exploring. Exploration is left out of that comparison so that an exploration's choice is never mistaken for the ceiling's effect.

## What it costs

**Some jobs that `max` would have finished take a second attempt, or come back to the caller.** Once a step up from `xhigh` has been used, there is no further step without asking, so a job only `max` could finish now ends with its caller instead of climbing on. That is the intended trade: the most expensive level is used only when someone chose it.

**An orchestrate run is not re-approved for a change of ceiling.** The ceiling is part of the run's routing account but not of the plan's approval identity, as with `--fast`. It changes which point is chosen, not which tickets are worked or how, so a different ceiling does not by itself need a new approval. A run cannot be resumed under a different ceiling, because the resume is refused before anything is claimed.
