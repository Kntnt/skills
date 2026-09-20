# Quota is a guard rather than a currency

This record decides how a subscription's weekly window enters Model Selector's answer. It does not: the ranking stays on list price, and the window instead narrows the pool before anything is ranked. A subscription channel is left out of a machine-chosen answer while its weekly window is more than ten points ahead of the share of the week elapsed, or at ninety per cent whatever the pace. `docs/rules/routing.md` states the rule as it applies now; this record explains why it has this shape (issue #373, out of #368).

## What ran out

**On 2026-09-19 six Codex attempts took a ChatGPT Pro 20x weekly window from 0 % to 13 %, and the ranking never noticed.** At roughly 10–13 list-price USD per percentage point, the ranking went on treating that channel as though the money were the constraint. It was not. The money is a number nobody was going to be billed for; what was actually finite was a window that, at that rate, would have been gone before the week was. A ranking that cannot see the thing that stops the work is a ranking that will keep spending it.

## Why a guard and not a currency

**Ranking on quota consumed was considered and set aside.** It is the obvious move — put the window into the arithmetic and let the frontier price it — and three things make a per-attempt figure mostly noise. The resolution is whole points, so most attempts move the figure by nought and the occasional one by one. Concurrent sessions each hold their own last-fetched value, so an attempt's apparent consumption includes whatever the sessions beside it spent. And the maintainer's own use runs beside a run, which the machine has no way to separate out. A number that noisy, given the authority to order a frontier, orders it by accident.

**The harm to prevent is the window running out, and that is a threshold rather than a price.** Nothing is bought by the difference between 40 % and 41 % used, so there is nothing for an exchange rate to convert. What matters is whether the pace will exhaust the week, and that is a question with a yes and a no. So the window decides membership — who is in the pool at all — and touches no figure anything is ordered on. One rule, one place, and the ranking is exactly what it was.

**The alternative kept the two kinds of scarcity distinguishable.** A dollar is fungible and a window is not: an unspent window is worth nothing next week, and an overspent one stops work a dollar would merely have made dearer. Folding the second into the first would have meant inventing a price for a week of somebody's subscription, which is a statement about what their work is worth and only they can make it — the same reason ADR-0189 refuses to convert a minute into a dollar.

## Why those two thresholds

**Ten points ahead of the week's own pace, rather than a fixed share.** A share alone cannot tell a channel that has been used hard on Monday from one that is running out on Saturday; the pace can, because the window's reset instant says how much of it is gone. Ten points is wide enough that an ordinary heavy morning does not hold a channel back for the rest of the day, and narrow enough to catch a pace that would exhaust the week while there is still a week to save. Nothing measured picked the number — there is one week of evidence and it is the week the guard exists because of — so it is a judgement, recorded as one, and it is a threshold rather than a tuned constant in an arithmetic.

**Ninety per cent whatever the pace, because late in a window the pace test alone admits a channel that is nearly out.** At 99 % of the week elapsed, a channel at 90 % used is nine points *behind* the pace and about to be spent. The tenth that is held back is what the work only this channel can do runs on: a user's own session, a model lock, and a pool that would otherwise be empty, all of which reach a held-back channel anyway.

## What the guard never does

**It never empties the pool.** Where holding back would leave the call no candidate, nothing is held back. A guard that answered `inherit` because the subscription was busy would have stopped the work over an optimisation, and this Skill answers every call it can parse (ADR-0182). The same posture makes every absence harmless: a machine with no figure has no guard, said nowhere in an answer and reported as a problem nowhere.

**It never applies to a model the user locked.** A `--model` is the user naming what they want, and an optimisation does not overrule an instruction — the rule a lock already has everywhere else in this module.

**It is invisible to everything downstream.** It narrows the pool before the deliberation ceiling, so the ceiling, the ranking, the exploration and any later way of trying a point all read the guarded pool and none of them has to know the guard exists. Where it changed which point was answered, the note says so and names the point it ruled out, judged against the same call ranked with every channel admitted — so that a reader who finds a dearer point chosen can tell the guard at work from an exploration or from the ranking's own verdict.

## Where the figures come from

**Two local sources and nothing else: no network call, no credential read, and the same behaviour for any user of the public collection.** A routing decision that depended on an account somebody had to hold would be a routing decision most of this collection's users could not have.

**Codex publishes its own window, so it is read.** Every `token_count` event in its session logs carries `rate_limits.primary` with the used share, the window's length and its reset instant. The read runs inside somebody else's turn, so it is bounded rather than complete — the twenty most recently modified logs, the last 64 KiB of each, scanned backwards for the last event carrying a window — and the machine-wide figure is the newest by the event's own timestamp, because concurrent sessions each hold their own last-fetched value.

**Claude Code publishes nothing a figure could be rebuilt from, so the machine writes one down as it goes.** Its transcripts carry no rate-limit fields. What it does have is a status line, handed the windows on standard input on every render — `rate_limits.seven_day.used_percentage` and `rate_limits.seven_day.resets_at`, documented at <https://code.claude.com/docs/en/statusline.md>. So the figure comes from a file the machine's own status line writes rather than from anything this Skill fetches.

**The status line that writes it is this collection's own, rather than a snippet `setup` offers to add.** The ticket's first draft had `setup` tee a `jq` line in front of whatever status line the user had. That could not work here: `statusLine` is a single-valued setting, `install_statusline` rewrites it whole on every convergence, and on a machine where the `statusline` Feature holds the slot the command being extended is this collection's own — so anything teed in front of it is discarded at the next Enable. The Feature writes the file instead, from the payload it has already read. Enabling `statusline` through the Manager is what arms the Claude channel's guard, and removing it is what disarms it. A user who has replaced the status line with their own, or has none, simply gets no guard for that channel, which is one of the absences the guard already treats as ordinary.

**The file is stale after a day, from either source.** A status line runs whenever a session renders and a Codex session writes one of those events every turn, so a figure older than that is from a machine nobody has worked on since — and on a seven-day window a day of drift is already worth more than the ten points the rule turns on. A week-old reading of ninety-five per cent holds nothing back.

## What it costs

**Work goes to a dearer channel while a cheaper one is rested.** That is the trade, taken deliberately: the dearer channel's money is a number on a list, and the rested channel's week is what the work actually runs on.

**One more read on every call.** A bounded directory listing and up to twenty tail reads, inside somebody else's turn. The bound is what makes that acceptable, and it is why a machine with years of sessions costs what a machine with a week's costs.

**The guard is on, with no flag and no standing setting to turn it off.** There is no second code path for a machine without the figures, because absence is already the answer there — and a switch would be a thing to explain, to document, and to find turned off on the machine where the window ran out.
