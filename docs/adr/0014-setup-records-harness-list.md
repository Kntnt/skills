# Setup records the Harness list

**Retired.** Setup, the Harness list, and the Unsatisfied state below are gone: targets are resolved by detection at each invocation (ADR-0035). The record is kept for the shape it explains — everything after this line describes how the collection used to work.

Enable, Disable, and Update need to know which Harnesses to touch. The Harness list is a decision, not State. If it is missing, the manager rebuilds it from Harnesses that already have a collection skill other than the Manager — a Harness that has only the Manager is ambiguous, because the transport always leaves the Manager there. Wrong inclusion would apply skills the user never chose for that Harness. If the rebuild finds no such Harness, the list is Unsatisfied: those subcommands stop and tell the user to run Setup. Status and Help do not stop.

Setup shows detected Harnesses pre-checked and may be run again. Adding a Harness applies every skill Enabled in Global, with no extra question (ADR-0005). Removing a Harness asks before deleting this collection's files there. The first Setup may hand off to Enable so the user can pick skills; that hand-off is optional and is the only time Setup talks about skills.
