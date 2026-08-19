# A run refuses a working tree it cannot account for

An unattended run commits. At a ceiling of one it commits on the branch the developer is standing on, in the working tree they left behind; above one it merges into that same branch. Both gestures assume the same thing about that tree: that everything in it either belongs to the run or is already committed.

Nothing checked it. A change the developer had not committed when the run started was therefore swept into whichever ticket's builder came first — the brief tells a builder to leave nothing uncommitted, and a builder cannot tell somebody else's work from its own — and the ticket was then closed on that commit. Above one it failed the other way about: an untracked file the merge would have written stopped `integrate` with no conflicted file to name, which the run reads as a collision, repairs, fails to verify, and answers with a rebuild it never needed.

**So the run asks the repository whether the tree is clean, and refuses where it is not.** It asks when it plans, which is where an unattended night is stopped before it starts, and again before a ticket is recorded done, which is the last moment work that was never committed can be told from work that was.

**A refusal, not a warning.** There is nobody awake to read a warning. The two outcomes it prevents — a ticket closed on a commit carrying somebody else's work, and a ticket rebuilt over a collision that never happened — are both indistinguishable from success in the report the developer wakes up to.

**Done is the only outcome the second gate holds back.** A ticket that failed leaves its work where it stands on purpose, so refusing to record a failure from a tree that still holds work would refuse the very outcome that tree is in that state to record.

**What the repository ignores is not work.** The question is `git status --porcelain`, which says nothing about an ignored file and nothing about the run's own working trees either — those live under the git directory (ADR-0054), where they were put so that this question would have a clean answer.

**What this costs.** A developer who keeps work in progress on the branch they want a run on has to commit or stash it first, and is told so by a plan that reports its whole scope and starts nothing.
