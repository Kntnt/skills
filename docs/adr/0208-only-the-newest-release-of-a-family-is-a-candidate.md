# Only the newest release of a family is a candidate

This record decides which releases of one model family Model Selector may answer with. Among the models a call would otherwise be answered with, only the newest release of each family is a candidate — the answer, the alternatives, the exploration and the step up after a failure alike. Nothing stored is touched and no lock is overridden. `docs/rules/routing.md` states the rule as it applies now; this record explains why it has this shape (issue #375, out of #368).

## What a maker's list is actually saying

**A maker's list is a catalogue of what it will still serve, not a recommendation of what to run.** OpenRouter lists `x-ai/grok-4.3` and `x-ai/grok-4.5` beside `x-ai/grok-4.6`, and there is no sign it will ever stop. Anthropic's and OpenAI's own lists behave the same way for as long as an account keeps access to a superseded release. The pool read that list as a list of candidates, so a release its own maker had replaced went on being ranked, offered as an alternative, explored, and stepped up to, indefinitely.

**The lifecycle rule does not reach it and was not the right tool.** ADR-0192 removes a model its maker stopped listing, with its measurement rows; these releases are still listed, so nothing about them is missing, and nothing about them is gone. The two rules answer different questions — *is this model still offered* and *is this release the one to use* — and folding the second into the first would have meant deleting evidence of a version that still exists and that a user may still want.

## Why the catalogue's own field, and nothing cleverer

**A family is whatever the catalogue's `family` field says.** The refresh pass writes it: the literal `grok` for each admitted `x-ai/` model, and for OpenAI the id's last alphabetic segment, which gives `sol`, `astra`, `terra` and `luna` their own lines. So `gpt-5.6-sol` and `gpt-6-astra` are two version lines however much their ids have in common, and `gpt-6-astra` is no newer Sol.

**Nothing infers a succession the catalogue does not state.** The alternative was a field saying that one family succeeds another — that Astra follows Sol, that `gpt-5.5` was replaced by `gpt-5.6-sol`. No structured source publishes such a fact, so it would have been kept by hand, for one model, and gone stale the first time a maker named a release something nobody predicted. The accepted cost is that a family the catalogue gives its own line keeps its candidacy: `gpt-5.5`, where a refresh builds one from the Codex list, stays a candidate under this rule. Its estimate for every kind measured so far sits far below anything measured, so it is never the plain answer, and that is a cheaper thing to accept than a hand-kept succession table.

**The comparison is lexical rather than numeric, for the same reason.** Reading a version number out of an id is inference about a naming scheme a maker may change without telling anybody. `released` decides, the id settles a tie, and both are compared as strings.

## Where the gate sits, and why not earlier

**It is the last gate, after both locks and after the deliberation ceiling.** The obvious place was the pool itself, where eligibility is decided. Three things break there.

**A family whose newest release this call cannot use would vanish instead of shrinking.** Two shapes produce that within one provider. A release the gateway its opencode channel pays through records no slug for has no route, `gateways` being a per-model field; and a release supporting no level at or below the deliberation ceiling has no point left. Filtered early, the family is represented by a release the call cannot start, and where that family is the only one in the pool the pool is emptied — which no gate of this module may do, this Skill answering every call it can parse (ADR-0182). Filtered last, the rule can only ever remove a release another release of the same family survives, so it empties no pool by construction.

**A lock's own note would disappear.** `_locked_to_model` writes *names several models; X is newest* off a count of matching ids in the pool it is handed. Narrow that pool first and the count is always one, and the promise that an alias naming several eligible releases takes the newest and says so stops being visible to anybody. Running the lock first also honours an exact-id lock with no exemption written for it: the pool is then that one release's points, and the rule has one release of the family to compare.

**The judge comes back through the same entry point.** `grade.py` runs `selection.py` for its own point, so there is exactly one place the rule has to be applied and no second reproduction of the pool to keep in step.

## The trade-off it settles

**An older release with rows loses to a newer one with none.** That runs against *a point measured for the kind comes before one only estimated* (ADR-0187), which is the strongest ordering rule this module has, and it is the real cost of this decision. The evidence about `grok-4.5` is evidence about `grok-4.5`; `grok-4.6` is a different model and the rows say nothing about it.

**It is taken anyway, because the alternative compounds.** A store that keeps answering with the release it has rows for buys every further row about that same release, so the newer one is never measured, so it never becomes the measured point, so the store is still answering with a superseded release a year later. Exploration does not fix it either: an exploration moves one dimension and buys a row, and it would go on buying rows about a frontier of releases nobody will run again. The rule is what lets the evidence move on with the world, and one call at each new release is what it costs.

## What it never does

**It never overrides a lock.** `--model` naming a release by its exact id is the user saying which one they want, and it is answered with that release. Nothing had to be written for it: the lock runs first and the rule then sees one release of the family. A family alias goes on resolving to the newest and saying so.

**It touches nothing stored.** A superseded release keeps its catalogue entry, its measurement rows, its pending units and its generated agent definition. Rows are evidence of a version that does not change, the entry is what a lock resolves against, and the definition is what a locked Claude Code call is launched by.

**It adds no note, no flag and no setting.** A family collapsing to its newest release is the ordinary state of a catalogue rather than an event worth telling a caller about, and there is no behaviour to switch off. What the rule does bind is the notes that already exist: none of the notes this Skill composes from the pool may name a release the rule removed, which is why the unceiled pool the ceiling is measured against is narrowed too. A note echoing a token the caller itself passed, on `--after` or on `--model`, is the caller's own word and is not one of those.

## One order, in one place

**`catalogue.newest_first` is the single comparison, and three callers go by it.** The family alias, the pool's choice of release and the subagent file name a family takes are three askings of *which release of this family is the newest*, and until now two of them answered a tie opposite ways: `resolve` sorted ascending by id under a stable descending sort on `released`, giving a tie to the smaller id, while `definitions` sorted descending on `(released, id)` and gave it to the greater. Written that way, a tie would have had a family alias and an unlocked call naming two different releases of one family off one catalogue. The kept order is `resolve`'s, an alias's answer being the one a user sees and types: newest by `released`, an undated entry older than every dated one, a tie to the smaller id. Nothing but a tie changes behaviour anywhere.
