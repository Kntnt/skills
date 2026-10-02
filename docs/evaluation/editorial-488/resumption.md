# Resumption of the interrupted #488 attempt

Attempt `ms-20261002-d7a4d2` resumes the same frozen plan and authorized roots. The plan-freeze (`80ffe252`) and failed-launch capture commit (`d497a4ce`) are base history and are not rewritten.

The previous attempt's `operator-interruption.json`, nine completed baseline packets with eighteen completed judgements, and three voided second-arm starts are preserved as received. The voids are operator/staging interruptions, not delivery findings. Their missing final inventories are gaps, not evidence of successful cleanup or completion. Separate `recovered-native-sessions/` and `recovery-inventory.json` files preserve the stopped roots as observed during resumption; they do not replace a missing completion packet.

The controller reported removing `/private/tmp/kntntnt-orchestrate-20261002.o7bmMK` after confirming the reported processes and groups were gone. This session neither removes that unauthorized path nor changes the earlier interruption account. The scratch alias resolves to `/private/tmp/kntnt-orchestrate-20261002.o7bmMK/ticket-488-scratch`; resumed tool caches and temporary environments use that physical root.

All six targeted baseline responses contain the artifact and report in the Harness's terminal reply. No baseline reproduction licenses a product wording change. The second arm therefore exports the same product revision, `5457c89405aece11b325937f9f07407f01974f7c`, under the existing plan. The nine second-arm rows start fresh; no completed baseline run or judgement is repeated.

The initial gate's four logs and command outcomes are preserved in `verification-initial/`. Its pytest failure is the prospective plan's citation to reserved ADR-0239 before that required record exists; 2732 tests passed. The final gate is a new measurement after evidence assembly, rather than a replacement of these results.

The first resumed full gate is preserved in `verification-resume-1/`. Ruff, formatting and mypy passed; pytest had 2732 passes and one failure because the repository registry fixture enumerated only the older retest captures. Staging #488's preserved numbered snapshots adds actual tracked registries. The fixture must include their exact captured maxima; the registry engine, its manifest-independent contract, the original maxima and all four gate commands stay unchanged. This is evidence-fixture maintenance, not a Redline or other Skill behavior change.

The final full gate is a separate measurement in `verification-final/`: all four unchanged commands pass, with 2733 pytest passes. The isolated registry check was observed green after the preserved red. Final campaign and process receipts are in `operator-receipts/`; evaluator teardown is recorded separately in `cleanup.json` and does not rewrite any native outcome.
