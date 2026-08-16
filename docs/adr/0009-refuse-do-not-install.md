# Skills refuse when a dependency is unsatisfied; they never install

Enable and Update put collection skills on disk only. They do not install Externals or runtime binaries. When a skill is used and a Dependency is Unsatisfied, the skill does no work and gives a short instruction the user can follow (Enable a collection skill via `/kntnt enable`, add an External via the transport, install a binary with that binary's own command). Auto-installing would take rights the user did not grant and would make the manager a package manager, which ADR-0001 forbids.
