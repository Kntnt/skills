# A Claude release read from the Harness list belongs to the family of its line

This record settles where a Claude release gets its family when the catalogue pass reads it from Claude Code's model list. [ADR-0208](0208-only-the-newest-release-of-a-family-is-a-candidate.md) made the catalogue's `family` field the only thing that says two releases are kin, and [ADR-0215](0215-a-newer-release-inherits-the-record-of-its-familys-older-releases.md) built the inheritance of rows on the same field. Neither record said how that field is written for a release the pass adds, and the pass wrote it wrong for every release the list names by its full id. What the rule now is is stated in [`docs/rules/routing.md`](../rules/routing.md). This record gives the reasons (issue #446).

## What the pass did

**On 2026-09-29 the pass added five superseded releases as families of their own.** Claude Code's answer to `initialize` names most entries by a family word: `opus`, `sonnet`, `haiku`. That day it also returned seven entries whose `value` is a full id: `claude-sonnet-5`, `claude-opus-5`, `claude-fable-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6` and `claude-sonnet-4-6`. `claude_reading` took the lower-cased `value` as the family. The two already in the catalogue kept the families they had. The five it lacked were entered with their own id as their family, and each had that id as its only alias. A read of the list a few minutes earlier, from another working directory, returned only the short entries. So the list can hand the pass pinned releases on one day and none on the next.

**Each of the five was out of the newest-release rule's reach.** The rule keeps the newest release of each family, and a family of one has no newer release. The pass wrote 23 subagent definitions for the five, `kntnt-claude-<id>-<level>.md`, next to the files of the releases that replaced them. The same day, `selection.py --kind=mechanical` answered `claude-sonnet-4-6` at `high` as a Trial, with `claude-sonnet-5-5` only as an alternative. `--kind=review` listed `claude-opus-4-7` among its alternatives. The maintainer's ruling that day: once a newer Sonnet exists, no older Sonnet is used at all, and where that is possible it is a bug. That is ADR-0208's rule, and it applies to every line.

## The rule

**A family word in the list is the family. For a full id, the family is the line the id names.** The line is the one word of the id that is neither `claude` nor a number or a date. So `claude-opus-4-8` is an `opus`, `claude-fable-5` a `fable`, and `claude-3-5-sonnet-20241022` a `sonnet`. The list's `value` is still the release's alias, so what Claude Code calls a release is still what a lock can name it by. Only the family changed.

**The pass corrects what it wrote before, from the id alone.** On every pass that reads the list, a Claude entry whose family is its own id is moved into its line, and the move is journalled. It does not matter whether that day's list returns the entry. A fix that waited for the list to name the release again could wait for ever, because the list returns pinned releases only on some reads. Nothing but the family moves. The release keeps its entry, its measurement rows and its pending Units, and the newer release of its line reads those rows as its inheritance, as ADR-0215 says.

**An id that names no one line is left as it is, and said.** An id with no such word, such as `claude-5`, or with two, keeps its own id as its family. The pass names it under `untold` in `refresh.json` on every pass, and in a journal row noted `family untold` on the pass it arrives. `/model-selector status` shows both.

## Why the line is read off the id

**ADR-0208 refused to read a version out of an id. This reads less than that.** Its reason was that a comparison of version numbers is a guess about a naming scheme a maker may change, and a wrong guess would silently decide which release is newer. That stays true, and this rule does not touch it: which release of a line is newer is still decided by `released`, with the id breaking a tie as a string. What is read off the id is only the line word. A change of naming scheme that hid the line word would leave a release untold and reported. It would not place the release in a wrong line.

**The list gives nothing better.** For an entry named by its full id, the only other field that could say which line it belongs to is its display name and description, which are prose. The short entries do name a family, but only for the release each word currently points at: `opus` resolves to Opus 5.5 and says nothing about Opus 4.8.

## The alternatives

**Pinned releases as deliberate candidates, each with definition files of its own.** The issue's second reading: the list lists older releases on purpose, and a lock such as `--model=claude-opus-4-8` should be able to start exactly that release through a file of its own. The maintainer rejected it. An older release in the pool is what the ruling forbids. A lock that names an older release by its exact id is still answered with that release, as ADR-0208 says. On Claude Code, the definition that starts it is the one its line's newest release owns.

**A table of known releases and their lines.** It would place the five correctly on the day it was written and would be wrong for every release after. The ruling asked for a rule that holds for a release nobody has seen yet, such as a future `claude-sonnet-5-6` or `claude-opus-6`, and a hand-kept table goes stale the day the next release ships.

**Dropping the full-id entries from the reading.** A release listed only by its full id would then never be added, even where it is the newest of its line. The pass would stop learning about new releases when the list named them that way. The ruling was about older releases, not about ignoring whatever the list says in that shape.

**Guessing a line for an id that names none.** A wrong line is worse than a family of one. A wrong line takes a release out of its own line's rule and puts it into another's, where it can hide that line's newest release. A family of one is visible, is named in every pass's report, and is still subject to every other gate.

## What this leaves out

**Removing the five.** They are still in Claude Code's list, so the catalogue keeps them. That is what a lock resolves against, and what ADR-0192's absence rule would remove them by if the list stopped returning them. Their files go, because definitions are named by family and level and the newest release of each line takes the name.

**GPT and Grok.** Codex's list names each model by its id and the pass takes the family from the id's last word, which ADR-0208's `gpt-6-astra` example depends on. Grok has one family. Neither had this fault, and neither changes.
