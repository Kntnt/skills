# The world's facts are fetched by the agent and adopted through the validator

[ADR-0182](0182-how-a-model-is-chosen-and-how-the-choice-is-measured.md) reversed an older rule and said that an unattended pass may learn what a model costs. The pass was built as that record describes it — conditional, one connection at a time, bounded against a monotonic clock, storing nothing it could not attribute — and it was then read against the maintainer's own machine on 2026-09-06. It had been running at the end of every session since it was installed, and it had never learned anything at all. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files; this record argues. ADR-0182 stands as written and describes the design at its own date.

## What the pass actually did

**It retrieved seven pages and interpreted none of them.** `refresh.py` reads `source-states.jsonl`, fetches whatever that store says has fallen due, and interprets a body only where the source's own `reads_as` member names a reader the script implements. There is exactly one reader, `catalogue-json`, and what it reads is a document already in this Skill's own catalogue shape. No provider publishes one. None of the seven sources on the maintainer's machine names any reader at all. So every pass since installation hashed a page, wrote the hash back, and stopped.

**`catalogue.json` had therefore never been written.** Prices, model lists, deliberation ladders and subscription plans could move only with a new release of `data/catalogue-seed.json` — which is to say, only when a human edited a file in this repository. That is precisely the silent inertness this Skill exists not to have: a machine confidently answering from a rate card nobody had revisited, with a maintenance mechanism installed, reporting healthy, and doing nothing.

**Nothing created a source row either.** The rebuild that produced the current Skill kept the pass and dropped whatever used to write `source-states.jsonl`. So the store could not grow, the one reader could not be reached, and the design had no path by which it could ever have started working.

**The price of that was 954 lines of code, a shipped cadence file, a store, and a network connection at the end of every session.** Read as a trade, it is the worst kind available: real cost, real surface, real complexity in the one path that runs inside somebody else's session, and no fact.

## Why no amount of parsing fixes it

**A script cannot read a pricing page, and the ones that try are worse than the ones that do not.** Provider pricing lives in rendered tables, marketing pages and documentation that is rewritten without notice. A scraper against it is either wrong quietly — which for a rate card means every ranking this Skill produces is wrong quietly — or it is a maintenance burden that outlives the person who wrote it. The `reads_as` design was an honest refusal to guess, and the honest refusal turned out to be the whole of the behaviour.

**The agent running `update` already has what the script lacks.** It holds a web tool, it reads a page the way a person does, and it is being asked to do exactly one bounded reading job at a moment a human asked for it. The brief this Skill was rebuilt from allowed this alternative from the start: fetching at `setup` and `update` is enough.

**What a machine is good at is deciding what may enter the store, not finding it.** That half stays a script and gets stricter rather than looser. The agent writes what it read as one document in the catalogue's own shape; `catalogue.py adopt` decides, per entry, whether it may be adopted at all.

## What the validator is for

**Every rule is per entry, so one bad row costs its own row.** An entry with nothing to attribute it to, a rate card in a currency other than USD or a unit other than per million tokens, a deliberation level off the ladder: each is discarded by name with the rule it failed, and the rest of the document is adopted. Refusing twenty good facts because the twenty-first was misread would make an honest agent's ordinary imperfection expensive, and would teach it to send less.

**Only a document that is not the catalogue's shape at all is refused whole.** At that point there is nothing to be per-entry about, and writing half of something unrecognised is worse than writing none of it.

**A model merges field by field and is written back complete.** `catalogue.load` merges seed and refreshed per id with the refreshed entry replacing the seeded one whole, so a partial entry written here is a fact the Skill silently stops knowing. `capability` is the one that matters: it is a seeded prior refined by measurement, nothing fetches it, and a merge that dropped it would disarm the estimate hierarchy's top level on the first successful `update`. Plans are replaced per provider whole, because a plan a provider stopped selling has to be able to disappear.

**A currency is refused rather than converted, here as everywhere else in this Skill.** Converting is a claim about an exchange rate on a date, and nothing in this collection has one. A card in euros added to a dollar bill is not a cheaper model; it is a wrong number that wins a ranking.

## What follows from moving the fetch

**`setup` opens with the same reading where the catalogue has gone stale.** The interview offers prices, model lists and plans as though they were current, and the user has no way to see that a list came from a release rather than from the provider. Thirty days on the newest `retrieved` date is when it is worth a reading first.

**`status` reports freshness from the dates the catalogue carries.** There is no source store to report on any more, and there does not need to be one: every model and every plan carries the address it was read from and the date it was read, which is a better account of how current the facts are than a table of when something was last checked. The three findings the pass used to make about the profile move there beside it.

**Nothing this collection installs reaches the network any more.** The per-turn hook path was already local; the session's last invocation now carries one bounded grading pass and nothing else. The network is reached by `update` and by `setup`, both of which a person asked for, and by nothing else at all — which is a simpler thing to say about somebody's machine than the bounded, conditional, credential-free pass it replaces, and it is true without qualification.

**`--force` goes with the cadence it forced.** There is no cadence left to ignore: a reading happens when somebody asks for one.
