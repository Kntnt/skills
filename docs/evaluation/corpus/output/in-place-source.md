# Why the runbook is in the repository

A runbook kept in a wiki is read at the moment somebody is least able to find it. It is behind a login, it is indexed by a search that ranks a two-year-old incident above this morning's procedure, and the person looking for it is already holding a terminal in the other hand.

The runbook that gets used is the one in the repository the service is deployed from, in the same directory as the thing it describes. It is reviewed in the pull request that changes the behaviour it documents, which is the only review that reliably happens, and it is available offline to whoever has already cloned the code. It is worse than a wiki at everything except being read during an incident, and being read during an incident is the whole job.
