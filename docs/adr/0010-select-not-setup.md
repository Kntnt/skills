# A skill change is Select, and there is still no Setup

The user changes what is Enabled by answering a list. `/kntnt select` prints the Catalog and takes the answer; there is no second verb to name a skill to and no name to carry from one command into another (ADR-0043). `--on` and `--off` name skills directly, for a machine with nobody there to read a list.

There is no Setup at all, and that half of this record has not changed. Which directories a change reaches is resolved by detection at each invocation (ADR-0035): never configured, never asked, never recorded. What the user chooses is which skills, in which layer. Where those skills land is not a choice the collection offers, so there is nothing left for a setup step to collect.
