# Target directories are detected at each invocation, never recorded

Enable, Disable, and Update have to know which skills directories to write to. Recording that answer — a verb that asks it, a file that remembers it, a failure state for when it is missing — buys less than the transport's own default gives away for free, and it goes stale the day another Harness is installed. So nothing is recorded. Each invocation resolves its targets from what is on the disk in front of it.

A Harness is present in a layer when it has a home there: the parent of its skills directory exists — `~/.claude` for Global, `.claude` in the working directory for Project. Presence is not the same as already holding skills, so a Harness installed after the last Enable is reached by the next Update with no configuration in between. Every present Harness is a target, and every call to the transport names the full set. Never a subset: the transport cannot remove a shared directory while another agent that reads it is left out of the call (issue #7), and a Manager that always names all of them never asks it to.

This is ADR-0030's rule applied one level up. A Skill that declares a Capability is Enabled everywhere and refuses where the Capability is Unsatisfied; a Skill that cannot work in some Harness says so when it is run rather than being kept off that disk in advance. Where a Skill goes stops being a choice; which Skills are Enabled remains the user's.

**All means all present, never all seventy-six.** The transport has the right rule and also a wrong fallback: detecting nothing, it targets every agent it knows of. Inheriting that would create skills directories for Harnesses the user has never installed — litter in a home directory and vandalism in a repository. With nothing detected the answer is the shared `.agents/skills` directory alone: the one the largest group of Harnesses reads, and the one the transport treats as canonical.

In the Project layer a Harness counts as present only when it keeps its skills under a hidden directory of its own. `skills`, `data/skills`, and `agent/skills` are things a repository has for its own reasons, and a rule that claimed them would write this collection into someone else's source tree on the strength of a name collision.

What this costs is real and was accepted: there is no longer a way to say *I have this Harness but I do not want the collection's Skills in it*. The remaining control is coarser and sits one level up — do not Enable the Skill at all, for anywhere.
