# The catalogue pass runs daily by itself, and reaches only structured sources

This record supersedes [ADR-0185](0185-the-worlds-facts-are-fetched-by-the-agent-and-adopted-through-the-validator.md) on one conclusion: that nothing this collection installs reaches the network unattended. [ADR-0191](0191-a-script-keeps-the-catalogue-current-from-three-structured-sources.md) named the three structured sources the catalogue pass reads and left the pass to be run by hand. This record schedules it. What the rules now are is stated in [`docs/rules/routing.md`](../rules/routing.md) and in the Skill's own shipped files. This record argues the case.

## What changed

**A pass nobody runs keeps nothing current.** ADR-0191 made `catalogue.py refresh` able to learn a new model and a new price with no agent and no web page, and then it had to be remembered. That is the same silent inertness ADR-0185 found in the design it replaced: a maintenance mechanism nobody drives, answering from a rate card nobody revisited. The maintainer wants the pass to happen once a day with nobody tending it (#312).

**ADR-0185's rule rested on a reason these sources do not have.** It kept the network out of anything unattended because a script cannot interpret a page, and a scraper is either quietly wrong or a burden that outlives its author. Structured data needs no interpreting. A harness's model list is a JSON answer to a protocol request, and OpenRouter's list is a JSON document with a published shape. The reason still holds for pages, and so does the rule for them.

## The rule

**The unattended pass reaches the three structured sources and nothing else.** They are Claude Code's answer to `initialize`, Codex's `model/list`, and OpenRouter's public `GET /api/v1/models`, exactly as ADR-0191 names them. The pass never runs a model and never reads a web page. Reading a provider's pages stays `update`'s, and happens only when a person asks for it.

**Enabling installs the job and Disabling removes it.** The job is a user LaunchAgent, `com.kntnt.model-selector.refresh`, under `~/Library/LaunchAgents/`. Its label carries its owner, so removal boots out that one label, deletes that one file, and leaves every other job alone. The operating system runs it, not a Harness, so there is one job per machine: any install puts it in place, whatever Harness it names, and only the removal the Manager makes when the Skill is Disabled takes it away. The mechanics live in the Collection Library beside the Harness adapters, as ADR-0177 places installation mechanics. Where the operating system has no adapter, the job is reported Unsatisfied and the Skill works as it did, the pass run by hand.

**It runs at 05:00 local time and at load.** The plist carries the absolute path of `uv` and the `PATH` of the process that installed it, because launchd's default `PATH` finds neither `uv` nor the harness CLIs the pass asks for their lists. It runs `catalogue.py refresh --scheduled` against the default data directory and never carries `--data`.

**Every bound is local to the machine.**

- One pass runs at a time per data directory, under `refresh.lock`.
- The scheduled entry point makes one attempt per UTC day. `refresh-marker.json` records it when a scheduled pass ends, whatever its outcome.
- Each source is given the lesser of thirty seconds and what remains of three hundred for the whole pass. A harness exchange runs in its own process group, killed at its deadline, and OpenRouter's pages share one budget as their socket timeout.
- The whole deadline is checked before the first write of any kind. A pass past it writes nothing but its marker. Applying is local and bounded, and once begun it is never interrupted.
- A SIGTERM, which is what `launchctl bootout` sends a running job, releases the lock and writes no marker.

**The marker gates only the scheduled entry point.** A pass a person starts always runs, under the same lock and the same deadlines. Somebody who asks for a pass wants one, whatever the clock has already done that day.

**A rehearsal never reaches the real account.** `launchctl bootstrap`, `bootout` and `print` are issued only where the plist lies inside the real user's home, as the password database names it. `$HOME` does not decide this. A Manager Sandbox redirects `$HOME` to rehearse an install, and a test writes under a temporary root, so both write the plist and load nothing.

**Install converges without killing a pass.** Some installs find the plist already matching on the job's own keys: its label, its calendar interval, `RunAtLoad`, and the arguments after the script. Where launchd also holds the job, install rewrites the file and reloads nothing, because a reload boots out a pass that may be mid-run. Neither the `uv` path nor the script's path is compared. Several placed copies of the Skill would otherwise flap the job between healthy and degraded, and between reloads, for ever.

## Why launchd's calendar interval

**A session's end is not a daily execution on an idle machine.** A due check run at session end refreshes a machine only on days somebody works on it (`docs/research/model-lifecycle-2026-09.md`, section 3). It would also put a pass that may take three hundred seconds inside a moment Codex cuts to three.

**`StartCalendarInterval` coalesces the firings missed during sleep into one run on wake, and `StartInterval` loses them** (`launchd.plist(5)`). A laptop asleep at 05:00 still gets that day's pass.

**`RunAtLoad` covers a Mac that was off.** No scheduler runs while the machine is powered off. Loading at login runs that day's pass, and the marker makes a second run that day harmless. `RunAtLoad` also fires at Enabling and whenever the Manager's refresh reloads a changed job. That is intended, since the first pass then comes at once rather than the next morning.

## Why a day with no complete pass counts against removal

**The marker is written whatever the outcome, and a pass past its deadline writes nothing else.** For [ADR-0192](0192-a-model-its-maker-stops-listing-is-removed-with-its-measurement.md), that day is therefore a day with no complete read, which breaks a model's run of absent days rather than extending it. Deletion cannot be undone, so the bound fails in the direction that keeps things. No deletion ever follows a deadline.

## The alternatives

**A 24-hour due check at session end.** Rejected, for the two reasons above: it is not daily on an idle machine, and session end is a three-second moment on Codex.

**`cron`.** Rejected. It skips a time the machine slept through, which on a laptop is most early mornings, and launchd is the scheduler macOS itself maintains.

**Scheduling `update`'s reading of pages too.** Rejected. That reading needs an agent to interpret prose, which is exactly what ADR-0185 declined to trust unattended, and it would spend model calls with nobody watching. Plans stay `update`'s, since no structured source lists them.

**Loading the job wherever `$HOME` points.** Rejected. A Manager Sandbox redirects `$HOME` precisely so that a rehearsal changes nothing real, and a job loaded from a rehearsal would run against the real account every morning. Keying the gate on where the file is written, against the password database's home, is what keeps a rehearsal a rehearsal.

**Adapters for other operating systems now.** Left out. The machines this collection runs on are Macs. A systemd user timer with `Persistent=true` would be Linux's adapter, and until one exists the job is reported Unsatisfied there.
